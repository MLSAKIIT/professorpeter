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

  async generateScript(request: VideoRequest): Promise<ApiResponse<{ script: string; video_id: string }>> {
    return this.request('/api/generate-script', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateVideo(request: VideoRequest): Promise<ApiResponse<GeneratedVideo>> {
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

  async getVideoStatus(videoId: string): Promise<ApiResponse<{ status: string; progress: number }>> {
    return this.request(`/api/video/${videoId}/status`);
  }

  async downloadVideo(videoId: string): Promise<string> {
    return `${API_BASE_URL}/api/video/${videoId}/download`;
  }

  // Health check
  async healthCheck(): Promise<ApiResponse<{ status: string }>> {
    return this.request('/health');
  }
}

export const apiService = new ApiService();

// Mock data for development (when backend is not connected)
export const mockGenerateVideo = async (prompt: string): Promise<GeneratedVideo> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  return {
    id: Date.now().toString(),
    script: `Hey there, folks! Peter Griffin here with another mind-blowing explanation about "${prompt}". Now, I know what you're thinking - "Peter, how do you know so much about this stuff?" Well, let me tell you, it's because I once saw a documentary about it while eating a sandwich. So basically, ${prompt} is like when you're trying to explain something to Meg, but she just doesn't get it, you know? It's all about the science and stuff. Trust me on this one, I'm basically an expert now.`,
    shareUrl: `https://profpeters.app/video/${Date.now()}`,
    status: 'completed'
  };
}; 