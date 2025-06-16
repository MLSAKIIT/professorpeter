'use client';

import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface TemplateSelectorProps {
  selectedTemplate: number;
  onTemplateSelect: (templateId: number) => void;
}

const TemplateSelector: React.FC<TemplateSelectorProps> = ({ 
  selectedTemplate, 
  onTemplateSelect 
}) => {
  const templates = [
    {
      id: 1,
      name: "Educational",
      description: "Perfect for learning content",
      preview: "/template-1.png",
      icon: "🎓",
      gradient: "from-blue-500 to-cyan-500"
    },
    {
      id: 2,
      name: "Comedy",
      description: "Funny explanations",
      preview: "/template-2.png",
      icon: "😂",
      gradient: "from-purple-500 to-pink-500"
    },
    {
      id: 3,
      name: "Motivational",
      description: "Inspiring content",
      preview: "/template-3.png",
      icon: "💪",
      gradient: "from-orange-500 to-red-500"
    }
  ];

  const handlePrevious = () => {
    // In a real implementation, this would cycle through more templates
    console.log('Previous template');
  };

  const handleNext = () => {
    // In a real implementation, this would cycle through more templates
    console.log('Next template');
  };

  return (
    <div className="relative">
      <div className="flex items-center justify-center gap-8">
        {/* Previous Arrow */}
        <button
          onClick={handlePrevious}
          className="text-gray-400 hover:text-blue-400 transition-all duration-300 p-3 rounded-full hover:bg-gray-800/50 backdrop-blur-sm border border-gray-700/50"
        >
          <ChevronLeft size={28} />
        </button>

        {/* Template Cards */}
        <div className="flex gap-8">
          {templates.map((template) => (
            <div
              key={template.id}
              onClick={() => onTemplateSelect(template.id)}
              className={`
                template-card cursor-pointer rounded-2xl overflow-hidden w-56 h-80 relative
                ${selectedTemplate === template.id ? 'selected' : ''}
              `}
            >
              {/* Background Gradient */}
              <div className={`absolute inset-0 bg-gradient-to-br ${template.gradient} opacity-10`}></div>
              
              {/* Content */}
              <div className="relative z-10 h-full flex flex-col items-center justify-center p-6">
                {/* Icon */}
                <div className="w-20 h-20 rounded-2xl bg-gray-700/50 backdrop-blur-sm border border-gray-600/50 flex items-center justify-center mb-6 transition-transform duration-300 group-hover:scale-110">
                  <span className="text-4xl">{template.icon}</span>
                </div>
                
                {/* Template Info */}
                <div className="text-center">
                  <h3 className="text-white font-bold text-xl mb-2">{template.name}</h3>
                  <p className="text-gray-300 text-sm leading-relaxed">{template.description}</p>
                </div>

                {/* Preview Indicator */}
                <div className="mt-6 flex gap-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                  <div className="w-2 h-2 bg-pink-400 rounded-full"></div>
                </div>
              </div>
              
              {/* Selection Indicator */}
              {selectedTemplate === template.id && (
                <div className="absolute top-4 right-4 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center shadow-lg shadow-blue-500/50">
                  <span className="text-white text-sm font-bold">✓</span>
                </div>
              )}

              {/* Hover Effect Overlay */}
              <div className="absolute inset-0 bg-blue-500/5 opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none"></div>
            </div>
          ))}
        </div>

        {/* Next Arrow */}
        <button
          onClick={handleNext}
          className="text-gray-400 hover:text-blue-400 transition-all duration-300 p-3 rounded-full hover:bg-gray-800/50 backdrop-blur-sm border border-gray-700/50"
        >
          <ChevronRight size={28} />
        </button>
      </div>

      {/* View All Button */}
      <div className="text-center mt-8">
        <button className="text-blue-400 hover:text-blue-300 transition-all duration-300 text-base font-medium px-6 py-2 rounded-full border border-blue-400/30 hover:border-blue-400/60 backdrop-blur-sm">
          View All Templates
        </button>
      </div>
    </div>
  );
};

export default TemplateSelector; 