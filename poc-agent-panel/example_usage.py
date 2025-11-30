#!/usr/bin/env python3
"""
Example usage of the Panel Discussion class
Shows how to use the panel discussion programmatically
"""

from panel_discussion import PanelDiscussion


def main():
    """Run example panel discussions"""
    
    # Example problems to discuss
    problems = [
        "Should we build our new application using serverless architecture or traditional containers?",
        "How should we approach building a real-time data processing platform for IoT devices?",
        "What is the best strategy for migrating our monolithic application to microservices?",
    ]
    
    # You can also run just one problem
    problem = problems[0]
    
    print("Starting panel discussion...")
    print(f"Problem: {problem}\n")
    
    try:
        # Initialize the panel with AWS profile
        panel = PanelDiscussion(aws_profile="chrismiller")
        
        # Run the complete 4-round discussion
        panel.run_discussion(problem)
        
        # Access discussion history if needed
        print("\n\nDiscussion Summary:")
        print(f"Total responses: {len(panel.discussion_history)}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. Your AWS profile 'chrismiller' is configured")
        print("2. You have Bedrock access enabled")
        print("3. Claude Sonnet 4.5 model is available")
        print("\nRun 'python test_credentials.py' to verify your setup")


if __name__ == "__main__":
    main()
