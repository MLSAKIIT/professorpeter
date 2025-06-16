'use client';

import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, Copy, Share2 } from 'lucide-react';
import TemplateSelector from './TemplateSelector';
import VideoResult from './VideoResult';
import { mockGenerateVideo } from '@/lib/api';

interface GeneratedVideo {
  id: string;
  script: string;
  videoUrl?: string;
  shareUrl: string;
}

const VideoGenerator = () => {
  const [currentStep, setCurrentStep] = useState<'input' | 'result'>('input');
  const [selectedTemplate, setSelectedTemplate] = useState<number>(1);
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState<GeneratedVideo | null>(null);

  const handleGenerateVideo = async () => {
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    
    try {
      const mockVideo = await mockGenerateVideo(prompt);
      setGeneratedVideo(mockVideo);
      setCurrentStep('result');
    } catch (error) {
      console.error('Failed to generate video:', error);
      // Handle error state here if needed
    } finally {
      setIsGenerating(false);
    }
  };

  const handleBackToInput = () => {
    setCurrentStep('input');
    setGeneratedVideo(null);
    setPrompt('');
  };

  if (currentStep === 'result' && generatedVideo) {
    return (
      <VideoResult 
        video={generatedVideo}
        onBack={handleBackToInput}
      />
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl relative z-10">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <div className="glass-card rounded-2xl p-8 mb-8">
          <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
            Meet Peter — your video explainer on demand!
          </h1>
          <p className="text-gray-300 text-xl leading-relaxed max-w-3xl mx-auto">
            Pick a template. Type nonsense. Watch Peter struggle to explain it.
          </p>
          <div className="mt-6 flex justify-center">
            <div className="flex items-center gap-2 text-blue-400">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
              <span className="text-sm">AI-Powered • Peter Griffin Style • Instant Results</span>
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>

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
                <p className="text-gray-400 text-sm mt-2">This might take a moment while he figures things out</p>
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
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
          </p>
          <p className="mb-4">
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </p>
          <div className="mt-6 pt-6 border-t border-gray-600">
            <p className="text-blue-400 font-medium italic text-lg">
              Welcome to PeterTalks • Where prompts die and videos cry.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoGenerator; 