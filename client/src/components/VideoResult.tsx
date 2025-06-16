'use client';

import React, { useState } from 'react';
import { Copy, Share2, ArrowLeft } from 'lucide-react';

interface GeneratedVideo {
  id: string;
  script: string;
  videoUrl?: string;
  shareUrl: string;
}

interface VideoResultProps {
  video: GeneratedVideo;
  onBack: () => void;
}

const VideoResult: React.FC<VideoResultProps> = ({ video, onBack }) => {
  const [copySuccess, setCopySuccess] = useState(false);

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(video.shareUrl);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      console.error('Failed to copy: ', err);
    }
  };

  const handleShare = (platform: string) => {
    const encodedUrl = encodeURIComponent(video.shareUrl);
    const encodedText = encodeURIComponent("Check out this Peter Griffin explanation!");
    
    const shareUrls = {
      twitter: `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}`,
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`,
      linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}`
    };

    if (shareUrls[platform as keyof typeof shareUrls]) {
      window.open(shareUrls[platform as keyof typeof shareUrls], '_blank');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl relative z-10">
      <div className="mb-8">
        <button
          onClick={onBack}
          className="flex items-center gap-3 text-gray-400 hover:text-white transition-all duration-300 glass-card px-4 py-2 rounded-xl hover:scale-105"
        >
          <ArrowLeft size={20} />
          <span className="font-medium">Back to Generator</span>
        </button>
      </div>

      <div className="text-center mb-12">
        <div className="glass-card rounded-2xl p-8">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 bg-gradient-to-r from-green-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
            Here's your video. It exists. Why? That's on you.
          </h1>
          <div className="flex justify-center items-center gap-2 mt-4">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-gray-300">Video Generated Successfully</span>
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-12">
        {/* Video Preview */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white">Video Preview</h3>
            <div className="flex gap-2">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
          </div>
          <div className="aspect-video bg-black/50 backdrop-blur-sm rounded-xl border border-gray-600/50 flex items-center justify-center">
            {video.videoUrl ? (
              <video 
                src={video.videoUrl} 
                controls 
                className="w-full h-full rounded-xl"
              />
            ) : (
              <div className="text-center text-gray-400">
                <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg shadow-blue-500/25">
                  <span className="text-3xl">🎬</span>
                </div>
                <p className="text-lg font-medium mb-2">Video Processing...</p>
                <p className="text-sm">Peter is putting the finishing touches</p>
              </div>
            )}
          </div>
        </div>

        {/* Script */}
        <div className="glass-card rounded-2xl p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white">Generated Script</h3>
            <span className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-3 py-1 rounded-full text-sm font-medium">
              ✨ AI Generated
            </span>
          </div>
          <div className="bg-black/50 backdrop-blur-sm rounded-xl p-6 max-h-96 overflow-y-auto border border-gray-600/50">
            <p className="text-gray-300 leading-relaxed text-sm">
              {video.script}
            </p>
          </div>
        </div>
      </div>

      {/* Share Section */}
      <div className="glass-card rounded-2xl p-8 text-center">
        <h2 className="text-3xl font-bold text-white mb-2 bg-gradient-to-r from-pink-400 to-red-500 bg-clip-text text-transparent">
          Share it NOW
        </h2>
        <p className="text-gray-400 mb-8">Spread the Peter Griffin wisdom to the world!</p>
        
        <div className="flex flex-col items-center gap-8">
          {/* Copy Link */}
          <div className="flex items-center gap-4 w-full max-w-lg">
            <div className="glass-card rounded-xl px-4 py-3 flex-1">
              <span className="text-gray-400 text-sm truncate block">
                {video.shareUrl}
              </span>
            </div>
            <button
              onClick={handleCopyLink}
              className={`modern-button px-6 py-3 rounded-xl font-bold transition-all duration-300 ${
                copySuccess ? 'bg-green-500 hover:bg-green-600' : ''
              }`}
            >
              {copySuccess ? 'Copied!' : 'Copy Link'}
            </button>
          </div>

          {/* Social Share */}
          <div className="flex flex-col items-center gap-6">
            <p className="text-gray-400 font-medium">Or share it on social media</p>
            <div className="flex gap-6">
              <button
                onClick={() => handleShare('twitter')}
                className="w-14 h-14 bg-gradient-to-br from-blue-400 to-blue-600 hover:from-blue-500 hover:to-blue-700 rounded-2xl flex items-center justify-center transition-all duration-300 hover:scale-110 shadow-lg shadow-blue-500/25"
                aria-label="Share on Twitter"
              >
                <span className="text-white text-2xl">🐦</span>
              </button>
              <button
                onClick={() => handleShare('facebook')}
                className="w-14 h-14 bg-gradient-to-br from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 rounded-2xl flex items-center justify-center transition-all duration-300 hover:scale-110 shadow-lg shadow-blue-600/25"
                aria-label="Share on Facebook"
              >
                <span className="text-white text-2xl">📘</span>
              </button>
              <button
                onClick={() => handleShare('linkedin')}
                className="w-14 h-14 bg-gradient-to-br from-blue-700 to-blue-900 hover:from-blue-800 hover:to-blue-950 rounded-2xl flex items-center justify-center transition-all duration-300 hover:scale-110 shadow-lg shadow-blue-700/25"
                aria-label="Share on LinkedIn"
              >
                <span className="text-white text-2xl">💼</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* About Section */}
      <div className="glass-card rounded-2xl p-8 text-center mt-8">
        <h3 className="text-2xl font-bold text-white mb-6">About This Generation</h3>
        <div className="text-gray-300 text-base leading-relaxed max-w-4xl mx-auto">
          <p className="mb-4">
            This video was generated using advanced AI technology that captures Peter Griffin's unique 
            personality and speaking style. The script is created using state-of-the-art language models 
            trained to understand and replicate his humorous approach to explaining complex topics.
          </p>
          <p className="mb-4">
            Each generation is unique and tailored to your specific prompt, ensuring that every explanation 
            has Peter's signature blend of confidence and confusion that makes learning unexpectedly entertaining.
          </p>
          <div className="mt-6 pt-6 border-t border-gray-600/50">
            <p className="text-blue-400 font-medium italic text-lg">
              "Welcome to PeterTalks • Where prompts die and videos cry."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoResult; 