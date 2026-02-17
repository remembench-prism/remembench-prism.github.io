#!/usr/bin/env python3

import cv2
import os
from pathlib import Path

def convert_video_opencv(input_path, output_path):
    """Convert video using OpenCV with web-compatible codec"""
    try:
        # Open video
        cap = cv2.VideoCapture(input_path)
        
        if not cap.isOpened():
            return False, "Could not open video file"
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Use H.264 codec for web compatibility
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        if not out.isOpened():
            # Fallback to XVID if H264 doesn't work
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            out.write(frame)
            frame_count += 1
            
            # Progress indicator
            if frame_count % 100 == 0:
                print(f"  Processed {frame_count} frames...")
        
        # Release everything
        cap.release()
        out.release()
        return True, f"Success - {frame_count} frames processed"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    # Create videos directory
    output_dir = Path("static/videos")
    output_dir.mkdir(exist_ok=True)
    
    # Check input directory
    input_dir = Path("static/videos_orig")
    if not input_dir.exists():
        print("Error: static/videos_orig directory not found!")
        sys.exit(1)
    
    print("Converting videos using OpenCV with web-compatible codecs...")
    
    video_files = list(input_dir.glob("*.mp4"))
    total_files = len(video_files)
    
    successful = 0
    failed = 0
    
    for i, video_file in enumerate(video_files, 1):
        filename = video_file.name
        output_path = output_dir / filename
        
        print(f"[{i}/{total_files}] Converting: {filename}")
        
        if video_file.stat().st_size == 0:
            print(f"✗ Skipping empty file: {filename}")
            continue
        
        success, message = convert_video_opencv(str(video_file), str(output_path))
        
        if success:
            print(f"✓ Successfully converted: {filename} - {message}")
            successful += 1
        else:
            print(f"✗ Failed to convert: {filename} - {message}")
            failed += 1
    
    print(f"\nConversion complete!")
    print(f"Successfully converted: {successful}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    main()