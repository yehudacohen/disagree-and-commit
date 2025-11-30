import { useState } from 'react';
import type { FormEvent } from 'react';
import './ProblemInput.css';

interface ProblemInputProps {
  onSubmit: (problem: string) => void;
  isDebateInProgress: boolean;
  isLoading: boolean;
}

export function ProblemInput({ onSubmit, isDebateInProgress, isLoading }: ProblemInputProps) {
  const [problem, setProblem] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    
    // Don't submit if empty or debate is in progress
    if (!problem.trim() || isDebateInProgress) {
      return;
    }

    onSubmit(problem.trim());
  };

  // Input should be disabled during debate
  const isDisabled = isDebateInProgress;

  return (
    <div className="problem-input-container">
      <form onSubmit={handleSubmit} className="problem-input-form">
        <div className="input-wrapper">
          <input
            type="text"
            value={problem}
            onChange={(e) => setProblem(e.target.value)}
            placeholder="What do you want to build?"
            className="problem-input"
            disabled={isDisabled}
            aria-label="Engineering problem input"
          />
        </div>
        
        <button
          type="submit"
          className="summon-button"
          disabled={isDisabled || !problem.trim()}
          aria-label="Submit problem to panel"
        >
          {isLoading ? (
            <>
              <span className="loading-spinner" />
              <span>Assembling the panel...</span>
            </>
          ) : (
            'Summon the Panel'
          )}
        </button>
      </form>
    </div>
  );
}
