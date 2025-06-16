'use client';

import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Copy, Share2, Wifi, WifiOff } from 'lucide-react';
import TemplateSelector from './TemplateSelector';
import VideoResult from './VideoResult';
import { generateVideoWithBackend, getBackendStatus, checkVideoStatus } from '@/lib/api';
import { HeroSection } from './HeroSection';
import { cn } from '@/lib/utils';

interface GeneratedVideo {
  id: string;
  script: string;
  videoUrl?: string;
  shareUrl: string;
  status?: 'processing' | 'completed' | 'failed';
}

const VideoGenerator = () => {
  const [currentStep, setCurrentStep] = useState<'input' | 'result'>('input');
  const [selectedTemplate, setSelectedTemplate] = useState<number>(1);
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState<GeneratedVideo | null>(null);
  const [backendConnected, setBackendConnected] = useState<boolean | null>(null);
  const [statusMessage, setStatusMessage] = useState<string>('');

  // Check backend status on component mount
  useEffect(() => {
    checkBackendConnection();
  }, []);

  // Poll for video status if video is processing
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (generatedVideo && generatedVideo.status === 'processing') {
      interval = setInterval(async () => {
        const status = await checkVideoStatus(generatedVideo.id);
        if (status) {
          setStatusMessage(status.message || '');
          
          if (status.status === 'completed') {
            setGeneratedVideo(prev => prev ? {
              ...prev,
              status: 'completed',
              videoUrl: `/api/video/${prev.id}/download`
            } : null);
          } else if (status.status === 'failed') {
            setGeneratedVideo(prev => prev ? {
              ...prev,
              status: 'failed'
            } : null);
          }
        }
      }, 3000); // Check every 3 seconds
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [generatedVideo]);

  const checkBackendConnection = async () => {
    const status = await getBackendStatus();
    setBackendConnected(status.connected);
  };

  const handleGenerateVideo = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    setStatusMessage('Starting video generation...');
    
    try {
      const video = await generateVideoWithBackend(prompt, selectedTemplate);
      setGeneratedVideo(video);
      setCurrentStep('result');
      
      if (video.status === 'processing') {
        setStatusMessage('Video is being processed...');
      }
    } catch (error) {
      console.error('Failed to generate video:', error);
      setStatusMessage('Failed to generate video. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleBackToInput = () => {
    setCurrentStep('input');
    setGeneratedVideo(null);
    setPrompt('');
    setStatusMessage('');
  };

  if (currentStep === 'result' && generatedVideo) {
    return (
      <VideoResult 
        video={generatedVideo}
        onBack={handleBackToInput}
        statusMessage={statusMessage}
      />
    );
  }

  return (
    <>
    <HeroSection />
    <div className="relative flex h-full w-full  bg-black dark:bg-black">
          <div
            className={cn(
              "absolute inset-0",
              "[background-size:40px_40px]",
              "[background-image:linear-gradient(to_right,#262626_1px,transparent_1px),linear-gradient(to_bottom,#262626_1px,transparent_1px)]",
              "dark:[background-image:linear-gradient(to_right,#262626_1px,transparent_1px),linear-gradient(to_bottom,#262626_1px,transparent_1px)]",
            )}
          />
          <div className="pointer-events-none absolute inset-0 flex  justify-center bg-black [mask-image:radial-gradient(ellipse_at_center,transparent_5%,black)] dark:bg-black"></div>
    <div className="container mx-auto px-4 py-8 max-w-6xl relative z-10">

      {/* Backend Status Indicator */}
      {backendConnected !== null && (
        <div className="mb-6">
          <div className={`glass-card rounded-lg p-4 ${backendConnected ? 'border-green-500/30' : 'border-yellow-500/30'}`}>
            <div className="flex items-center gap-3">
              {backendConnected ? (
                <>
                  <Wifi className="h-5 w-5 text-green-400" />
                  <span className="text-green-400 font-medium">Backend Connected</span>
                  <span className="text-gray-400">• Real-time video generation available</span>
                </>
              ) : (
                <>
                  <WifiOff className="h-5 w-5 text-yellow-400" />
                  <span className="text-yellow-400 font-medium">Backend Offline</span>
                  <span className="text-gray-400">• Using demo mode with mock responses</span>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Template Selector */}
      <div className="mb-16">
        <TemplateSelector 
          selectedTemplate={selectedTemplate}
          onTemplateSelect={setSelectedTemplate}
        />
      </div>

      {/* Prompt Input Section */}
      <div className="glass-card rounded-2xl p-8 mb-8">
        <h2 className="text-3xl font-bold text-white mb-8 text-center">
          Enter your Prompts
        </h2>
        
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe Your Craziest doubts"
              className="modern-input w-full h-40 rounded-xl px-6 py-4 text-white placeholder-gray-400 resize-none focus:outline-none text-lg"
              disabled={isGenerating}
              maxLength={500}
            />
            <div className="mt-2 text-right">
              <span className="text-gray-400 text-sm">
                {prompt.length}/500 characters
              </span>
            </div>
          </div>

          <div className="text-center">
            <button
              onClick={handleGenerateVideo}
              disabled={!prompt.trim() || isGenerating}
              className={`modern-button text-white font-bold py-4 px-12 rounded-xl text-lg transition-all duration-300 ${
                isGenerating ? 'pulse-blue' : ''
              }`}
            >
              {isGenerating ? (
                <span className="flex items-center gap-3">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  Generating Videos...
                </span>
              ) : (
                'Generate Videos'
              )}
            </button>
          </div>

          {isGenerating && (
            <div className="mt-8 text-center">
              <div className="glass-card rounded-xl p-6">
                <div className="flex items-center justify-center gap-3 mb-3">
                  <div className="w-3 h-3 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-3 h-3 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-3 h-3 bg-pink-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
                <p className="text-gray-300 text-lg font-medium">Peter is working his magic...</p>
                <p className="text-gray-400 text-sm mt-2">
                  {statusMessage || "This might take a moment while he figures things out"}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* About Section */}
      <div className="glass-card rounded-2xl p-8 text-center">
        <h3 className="text-2xl font-bold text-white mb-6">About</h3>
        <div className="text-gray-300 text-base leading-relaxed max-w-4xl mx-auto">
          <p className="mb-4">
            Professor Peter is your AI-powered educational companion that transforms complex concepts into 
            entertaining and easy-to-understand video explanations. Using Peter Griffin's unique perspective, 
            we make learning fun and memorable.
          </p>
          <p className="mb-4">
            Simply enter your topic or question, choose a template style, and watch as Peter breaks down 
            even the most complicated subjects with his signature humor and surprisingly insightful explanations.
          </p>
          <div className="mt-6 pt-6 border-t border-gray-600">
            <p className="text-blue-400 font-medium italic text-lg">
              Welcome to PeterTalks • Where prompts die and videos cry.
            </p>
          </div>
        </div>
      </div>
    </div>
    </div>
    </>
  );
};

export default VideoGenerator; 