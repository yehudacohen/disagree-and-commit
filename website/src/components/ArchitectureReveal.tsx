import { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import './ArchitectureReveal.css';
import type { CostEstimate, AssetsFolder } from '../types';
import { getArchitectureDiagramUrl } from '../config/demo';

interface ArchitectureRevealProps {
  isRevealed: boolean;
  mermaidDiagram: string;
  costEstimate: CostEstimate;
  expertEndorsements: Record<string, string>;
  assetsFolder: AssetsFolder;
  onDownload: (assetType: 'diagram' | 'all') => void;
}

export function ArchitectureReveal({
  isRevealed,
  mermaidDiagram,
  costEstimate,
  expertEndorsements,
  onDownload
}: ArchitectureRevealProps) {
  const mermaidRef = useRef<HTMLDivElement>(null);
  const [diagramRendered, setDiagramRendered] = useState(false);
  const [renderError, setRenderError] = useState<string | null>(null);
  const [downloadSuccess, setDownloadSuccess] = useState<string | null>(null);

  // Initialize mermaid
  useEffect(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'dark',
      securityLevel: 'loose',
      fontFamily: 'monospace'
    });
  }, []);

  // Render mermaid diagram when revealed
  useEffect(() => {
    if (isRevealed && mermaidDiagram && mermaidRef.current) {
      const renderDiagram = async () => {
        try {
          setRenderError(null);
          const { svg } = await mermaid.render('mermaid-diagram', mermaidDiagram);
          if (mermaidRef.current) {
            mermaidRef.current.innerHTML = svg;
            setDiagramRendered(true);
          }
        } catch (error) {
          console.error('Mermaid rendering error:', error);
          setRenderError(error instanceof Error ? error.message : 'Failed to render diagram');
          setDiagramRendered(false);
        }
      };

      renderDiagram();
    }
  }, [isRevealed, mermaidDiagram]);

  // Export diagram as PNG
  const exportDiagramAsPNG = async () => {
    if (!mermaidRef.current) return;

    try {
      // Get the SVG element
      const svgElement = mermaidRef.current.querySelector('svg');
      if (!svgElement) {
        throw new Error('SVG element not found');
      }

      // Get SVG dimensions
      const bbox = svgElement.getBBox();
      const width = bbox.width;
      const height = bbox.height;

      // Create a canvas
      const canvas = document.createElement('canvas');
      const scale = 2; // Higher resolution
      canvas.width = width * scale;
      canvas.height = height * scale;
      const ctx = canvas.getContext('2d');
      
      if (!ctx) {
        throw new Error('Could not get canvas context');
      }

      // Scale for better quality
      ctx.scale(scale, scale);

      // Convert SVG to data URL
      const svgData = new XMLSerializer().serializeToString(svgElement);
      const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
      const svgUrl = URL.createObjectURL(svgBlob);

      // Load SVG into an image
      const img = new Image();
      img.onload = () => {
        // Draw white background
        ctx.fillStyle = '#1a1a2e';
        ctx.fillRect(0, 0, width, height);
        
        // Draw the image
        ctx.drawImage(img, 0, 0, width, height);

        // Convert canvas to blob
        canvas.toBlob((blob) => {
          if (blob) {
            // Create download link
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'disagree-and-commit-architecture.png';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Cleanup
            URL.revokeObjectURL(url);
            URL.revokeObjectURL(svgUrl);
            
            // Show success message
            setDownloadSuccess('Diagram downloaded successfully!');
            setTimeout(() => setDownloadSuccess(null), 3000);
          }
        }, 'image/png');
      };

      img.onerror = () => {
        URL.revokeObjectURL(svgUrl);
        throw new Error('Failed to load SVG image');
      };

      img.src = svgUrl;
    } catch (error) {
      console.error('Export error:', error);
      setDownloadSuccess('Failed to export diagram. Please try again.');
      setTimeout(() => setDownloadSuccess(null), 3000);
    }
  };

  // Download Mermaid source
  const downloadMermaidSource = () => {
    try {
      const blob = new Blob([mermaidDiagram], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'architecture-diagram.mmd';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      setDownloadSuccess('Mermaid source downloaded successfully!');
      setTimeout(() => setDownloadSuccess(null), 3000);
    } catch (error) {
      console.error('Download error:', error);
      setDownloadSuccess('Failed to download source. Please try again.');
      setTimeout(() => setDownloadSuccess(null), 3000);
    }
  };

  // Handle download button clicks
  const handleDownload = async (assetType: 'diagram' | 'all') => {
    if (assetType === 'diagram') {
      await exportDiagramAsPNG();
    } else {
      // Download both PNG and source
      await exportDiagramAsPNG();
      setTimeout(() => downloadMermaidSource(), 500);
    }
    
    // Call parent handler if provided
    onDownload(assetType);
  };

  if (!isRevealed) {
    return null;
  }

  return (
    <div className="architecture-reveal">
      <div className="architecture-container">
        <h2 className="architecture-title">The Final Architecture</h2>
        
        {/* Mermaid Diagram Section */}
        <div className="diagram-section">
          {getArchitectureDiagramUrl() ? (
            // Show image from URL if provided in demo config
            <div className="diagram-image-container">
              <img 
                src={getArchitectureDiagramUrl()} 
                alt="Architecture Diagram"
                className="architecture-diagram-image"
                style={{
                  maxWidth: '100%',
                  height: 'auto',
                  borderRadius: '8px',
                  boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)'
                }}
              />
            </div>
          ) : renderError ? (
            <div className="diagram-error">
              <p className="error-message">Failed to render diagram: {renderError}</p>
              <pre className="diagram-fallback">{mermaidDiagram}</pre>
            </div>
          ) : (
            <div 
              ref={mermaidRef} 
              className="mermaid-container"
              aria-label="Architecture diagram"
            />
          )}
        </div>

        {/* Cost Estimate Section */}
        <div className="cost-section">
          <h3 className="cost-title">Estimated Monthly Cost</h3>
          <div className="cost-total">
            ${costEstimate.monthly.toLocaleString()}
          </div>
          <p className="cost-note">{costEstimate.satiricalNote}</p>
          
          <div className="cost-breakdown">
            <h4>Service Breakdown</h4>
            {costEstimate.breakdown.map((service, index) => (
              <div key={index} className="service-item">
                <div className="service-header">
                  <span className="service-name">{service.service}</span>
                  <span className="service-cost">${service.cost.toLocaleString()}</span>
                </div>
                <p className="service-justification">{service.justification}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Expert Endorsements Section */}
        <div className="endorsements-section">
          <h3 className="endorsements-title">Expert Endorsements</h3>
          <div className="endorsements-grid">
            {Object.entries(expertEndorsements).map(([expertId, quote]) => (
              <div key={expertId} className={`endorsement-card expert-${expertId}`}>
                <div className="endorsement-quote">"{quote}"</div>
                <div className="endorsement-author">
                  - {expertId === 'jeff' ? 'Jeff Barr' : expertId === 'swami' ? 'Swami' : 'Werner Vogels'}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Download Section */}
        <div className="download-section">
          <button 
            className="download-button"
            onClick={() => handleDownload('diagram')}
            disabled={!diagramRendered}
          >
            Download Diagram
          </button>
          <button 
            className="download-button download-all"
            onClick={() => handleDownload('all')}
            disabled={!diagramRendered}
          >
            Download All Assets
          </button>
        </div>

        {/* Download Success Feedback */}
        {downloadSuccess && (
          <div className="download-feedback">
            {downloadSuccess}
          </div>
        )}
      </div>
    </div>
  );
}
