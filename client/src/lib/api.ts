// API configuration and service functions
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface VideoRequest {
  prompt: string;
  template_id?: number;
  duration?: number;
  key_points?: string[];
}

export interface GeneratedVideo {
  id: string;
  script: string;
  videoUrl?: string;
  shareUrl: string;
  status: 'processing' | 'completed' | 'failed';
}

export interface ScriptResponse {
  script: string;
  video_id: string;
  word_count: number;
  estimated_duration?: number;
  style?: string;
}

export interface StatusResponse {
  video_id: string;
  status: string;
  progress: number;
  message: string;
  created_at?: string;
  completed_at?: string;
  estimated_remaining?: number;
  current_step?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

class ApiService {
  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('API request failed:', error);
      return { 
        success: false, 
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  async generateScript(request: VideoRequest): Promise<ApiResponse<ScriptResponse>> {
    return this.request('/api/generate-script', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateVideo(request: VideoRequest): Promise<ApiResponse<any>> {
    return this.request('/api/generate-video', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateAll(request: VideoRequest): Promise<ApiResponse<any>> {
    return this.request('/api/generate-all', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getVideoStatus(videoId: string): Promise<ApiResponse<StatusResponse>> {
    return this.request(`/api/video/${videoId}/status`);
  }

  async downloadVideo(videoId: string): Promise<string> {
    return `${API_BASE_URL}/api/video/${videoId}/download`;
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string; dependencies: any }>> {
    return this.request('/health');
  }

  // Check if backend is available
  async checkBackendAvailable(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      return response.ok;
    } catch {
      return false;
    }
  }
}

export const apiService = new ApiService();

// Get download URL for a video
export const getVideoDownloadUrl = (videoId: string): string => {
  return `${API_BASE_URL}/api/video/${videoId}/download`;
};

// Enhanced video generation function that tries backend first, falls back to mock
export const generateVideoWithBackend = async (prompt: string, templateId?: number): Promise<GeneratedVideo> => {
  try {
    // First, check if backend is available
    const backendAvailable = await apiService.checkBackendAvailable();
    
    if (backendAvailable) {
      console.log('🚀 Using real backend for video generation');
      
      // Start video generation process directly (this includes script generation)
      const videoResult = await apiService.generateVideo({ 
        prompt, 
        template_id: templateId || 1 
      });
      
      if (videoResult.success && videoResult.data) {
        const { video_id, message } = videoResult.data;
        
        return {
          id: video_id,
          script: 'Script will be generated as part of the video process...',
          shareUrl: `${window.location.origin}/video/${video_id}`,
          status: 'processing'
        };
      }
    }
    
    // Fallback to mock if backend is not available
    console.log('⚠️ Backend not available, using mock response');
    return await mockGenerateVideo(prompt);
    
  } catch (error) {
    console.error('Error in video generation:', error);
    // Fallback to mock on any error
    return await mockGenerateVideo(prompt);
  }
};

// Enhanced status checking with real backend
export const checkVideoStatus = async (videoId: string): Promise<StatusResponse | null> => {
  try {
    const backendAvailable = await apiService.checkBackendAvailable();
    
    if (backendAvailable) {
      const result = await apiService.getVideoStatus(videoId);
      if (result.success && result.data) {
        return result.data;
      }
    }
    
    // Return mock status if backend unavailable
    return {
      video_id: videoId,
      status: 'completed',
      progress: 100,
      message: 'Video generation completed (mock)',
      created_at: new Date().toISOString()
    };
    
  } catch (error) {
    console.error('Error checking video status:', error);
    return null;
  }
};

// Mock data for development (when backend is not connected)
export const mockGenerateVideo = async (prompt: string): Promise<GeneratedVideo> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  const videoId = Date.now().toString();
  
  return {
    id: videoId,
    script: `Hey there, folks! Peter Griffin here with another mind-blowing explanation about "${prompt}". 

Now, I know what you're thinking - "Peter, how do you know so much about this stuff?" Well, let me tell you, it's because I once saw a documentary about it while eating a sandwich. 

So basically, ${prompt} is like when you're trying to explain something to Meg, but she just doesn't get it, you know? It's all about the science and stuff. 

The key thing to understand is that ${prompt} works in a very specific way - kinda like how my brain works, but actually functional. Trust me on this one, I'm basically an expert now.

And that's pretty much everything you need to know about ${prompt}. Remember, if Peter Griffin can understand it, so can you!`,
    shareUrl: `${typeof window !== 'undefined' ? window.location.origin : 'https://profpeters.app'}/video/${videoId}`,
    status: 'completed'
  };
};

// Backend connection status
export const getBackendStatus = async (): Promise<{
  connected: boolean;
  health?: any;
  error?: string;
}> => {
  try {
    const healthResult = await apiService.healthCheck();
    
    if (healthResult.success) {
      return {
        connected: true,
        health: healthResult.data
      };
    } else {
      return {
        connected: false,
        error: healthResult.error
      };
    }
  } catch (error) {
    return {
      connected: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}; 