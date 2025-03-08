# Manim Video Project

This repository contains the code and resources for creating a YouTube video using Manim (Mathematical Animation Engine).

## Overview

Manim is an animation engine for explanatory math videos designed by Grant Sanderson for his YouTube channel [3Blue1Brown](https://www.youtube.com/c/3blue1brown). This project uses the community-maintained version of Manim.

## Project Structure

- `scripts/`: Contains the script(s) for the video
- `src/`: Contains the Manim source code for the video animations
- `media/`: Output directory for rendered videos and images (gitignored)

## Setup

### Prerequisites

- Docker
- Docker Compose (recommended for easier setup)

### Using Docker

1. Build and run the Docker container:
   ```bash
   docker-compose up -d
   ```

2. Enter the container shell:
   ```bash
   docker-compose exec manim bash
   ```

3. Run a Manim scene:
   ```bash
   manim -p src/example_scene.py ExampleScene
   ```

### Rendering Options

- `-p`: Preview the output video
- `-ql`: Low quality (faster rendering)
- `-qm`: Medium quality
- `-qh`: High quality
- `-qk`: 4K quality

## License

See the [LICENSE](LICENSE) file for details.