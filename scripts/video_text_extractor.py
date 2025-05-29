#!/usr/bin/env python3
"""
Module for extracting text from YouTube videos using OCR.
Can be used as a standalone script or imported by other scripts.
"""

import cv2
import pytesseract
import yt_dlp
import os
import time
import shutil
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class VideoTextExtractor:
    def __init__(self, temp_dir=None):
        """Initialize the extractor with a temporary directory for processing."""
        # Use environment variable for temp directory if not provided
        if temp_dir is None:
            temp_dir = os.getenv('OCR_TEMP_DIR', "temp_video_processing")
        
        self.temp_dir = temp_dir
        self.frames_dir = os.path.join(temp_dir, "frames")
        
    def extract_text_from_video(self, youtube_url, frame_rate=None, cleanup=True):
        """
        Extract text from a YouTube video.
        
        Args:
            youtube_url: URL of the YouTube video
            frame_rate: Number of frames to extract per second
            cleanup: Whether to delete temporary files after processing
            
        Returns:
            Dictionary with extracted text and metadata
        """
        # Use environment variable for frame rate if not provided
        if frame_rate is None:
            frame_rate = float(os.getenv('OCR_FRAME_RATE', 0.5))
            
        try:
            # Create temporary directories
            os.makedirs(self.temp_dir, exist_ok=True)
            os.makedirs(self.frames_dir, exist_ok=True)
            
            # Download video
            print(f"Downloading video: {youtube_url}")
            video_path = self._download_youtube_video(youtube_url)
            
            # Extract frames
            print("Extracting frames...")
            num_frames = self._extract_frames(video_path, frame_rate)
            print(f"Extracted {num_frames} frames")
            
            # Perform OCR
            print("Performing OCR on frames...")
            extracted_text = self._perform_ocr_on_frames()
            
            # Compile results
            result = {
                "youtube_url": youtube_url,
                "frames_processed": num_frames,
                "extracted_text": extracted_text
            }
            
            # Clean up temporary files if requested
            if cleanup:
                print("Cleaning up temporary files...")
                self._cleanup()
                
            return result
            
        except Exception as e:
            print(f"Error extracting text from video: {e}")
            # Clean up on error
            if cleanup:
                self._cleanup()
            return {"error": str(e)}
    
    def _download_youtube_video(self, url):
        """Download a YouTube video using yt-dlp."""
        output_path = os.path.join(self.temp_dir, "video.mp4")
        ydl_opts = {
            'format': 'best[height<=720]',  # Limit resolution to save bandwidth
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    
    def _extract_frames(self, video_path, frame_rate=1):
        """Extract frames from video at specified frame rate."""
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps / frame_rate)
        
        success, frame = video.read()
        count = 0
        frame_count = 0
        
        while success:
            if count % frame_interval == 0:
                frame_path = os.path.join(self.frames_dir, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(frame_path, frame)
                frame_count += 1
            
            success, frame = video.read()
            count += 1
        
        video.release()
        return frame_count
    
    def _perform_ocr_on_frames(self):
        """Perform OCR on extracted frames and return results."""
        results = []
        frame_files = sorted([os.path.join(self.frames_dir, file) 
                             for file in os.listdir(self.frames_dir) 
                             if file.endswith('.jpg')])
        
        for i, frame_path in enumerate(frame_files):
            # Read the image
            img = cv2.imread(frame_path)
            
            # Preprocess the image for better OCR results
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            # Perform OCR
            text = pytesseract.image_to_string(gray)
            
            # Add to results if text was found
            if text.strip():
                results.append({
                    "frame_number": i,
                    "text": text.strip()
                })
        
        return results
    
    def _cleanup(self):
        """Remove temporary files and directories."""
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Error cleaning up temporary files: {e}")


def extract_text_from_youtube(youtube_url, output_file=None, frame_rate=None):
    """
    Extract text from a YouTube video and optionally save to a file.
    This function can be called from other scripts.
    
    Args:
        youtube_url: URL of the YouTube video
        output_file: Path to save the results (optional)
        frame_rate: Number of frames to extract per second
        
    Returns:
        Dictionary with extracted text and metadata
    """
    # Use environment variable for frame rate if not provided
    if frame_rate is None:
        frame_rate = float(os.getenv('OCR_FRAME_RATE', 0.5))
        
    extractor = VideoTextExtractor()
    result = extractor.extract_text_from_video(youtube_url, frame_rate)
    
    # Save to file if requested
    if output_file:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to {output_file}")
    
    return result


def main():
    """Run as a standalone script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract text from YouTube videos using OCR.')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--output', '-o', help='Output file path (JSON)')
    parser.add_argument('--frame-rate', '-f', type=float, 
                        default=float(os.getenv('OCR_FRAME_RATE', 0.5)), 
                        help='Number of frames to extract per second (default: 0.5)')
    parser.add_argument('--temp-dir', '-t', 
                        default=os.getenv('OCR_TEMP_DIR', "temp_video_processing"), 
                        help='Temporary directory for processing')
    args = parser.parse_args()
    
    extractor = VideoTextExtractor(temp_dir=args.temp_dir)
    result = extractor.extract_text_from_video(args.url, args.frame_rate)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        # Print a summary of the results
        print(f"\nExtracted text from {len(result['extracted_text'])} frames:")
        for i, item in enumerate(result['extracted_text'][:3]):  # Show first 3 results
            print(f"\nFrame {item['frame_number']}:")
            print(item['text'][:200] + ('...' if len(item['text']) > 200 else ''))
        
        if len(result['extracted_text']) > 3:
            print(f"\n... and {len(result['extracted_text']) - 3} more frames with text")


if __name__ == "__main__":
    main()
