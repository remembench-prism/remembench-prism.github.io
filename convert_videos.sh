#!/bin/bash

# Create videos directory if it doesn't exist
mkdir -p static/videos

# Check if videos_orig directory exists
if [ ! -d "static/videos_orig" ]; then
    echo "Error: static/videos_orig directory not found!"
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install ffmpeg first."
    exit 1
fi

echo "Converting videos from static/videos_orig to static/videos..."

# Counter for progress tracking
total_files=$(find static/videos_orig -name "*.mp4" | wc -l)
current=0

# Process each MP4 file in videos_orig
for video in static/videos_orig/*.mp4; do
    if [ -f "$video" ]; then
        current=$((current + 1))
        filename=$(basename "$video")
        output_path="static/videos/$filename"
        
        echo "[$current/$total_files] Converting: $filename"
        
        # Skip files that are likely corrupted by checking file size first
        if [ ! -s "$video" ]; then
            echo "✗ Skipping empty file: $filename"
            continue
        fi
        
        # Basic encoding with minimal options to avoid issues
        ffmpeg -i "$video" -c:v libx264 -c:a aac -preset slow -crf 18 -y "$output_path"
        echo "output_path: $output_path"
        
        if [ $? -eq 0 ]; then
            echo "✓ Successfully converted: $filename"
        else
            echo "✗ Failed to convert: $filename (skipping)"
        fi
    fi
done

echo "Conversion complete!"
echo "Converted videos are now in static/videos/"