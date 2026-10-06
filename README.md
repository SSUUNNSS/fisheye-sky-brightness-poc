# Fisheye Sky Brightness Analysis PoC

## Overview

This small proof-of-concept explores the spatial distribution of relative brightness in hemispherical fisheye sky images.

The project was developed as a preliminary exercise for fisheye-based daylight and Environmental Light Field analysis.

The image is transformed into a polar representation and divided into angular sectors and radial regions. Relative pixel-intensity statistics are then calculated for each spatial region and visualized.

## Objectives

The PoC demonstrates a simple workflow for:

- reading and preprocessing fisheye sky images,
- identifying the circular hemispherical image region,
- converting Cartesian image coordinates into polar coordinates,
- dividing the image into azimuth sectors,
- dividing the image into radial rings,
- computing regional mean brightness values,
- visualizing spatial and directional brightness distributions.

## Method

A grayscale representation of the original image is used as a simplified proxy for relative brightness.

For each pixel, its position relative to the center of the fisheye image is described using:

- radial distance,
- angular direction.

The hemispherical image is divided into 36 angular sectors and 5 radial rings.

Mean pixel intensity is calculated for each spatial region.

The resulting information is visualized as:

1. the original fisheye image,
2. a spatial brightness map,
3. a polar plot showing mean brightness by direction,
4. a two-dimensional spatial brightness matrix.

## Important Limitation

Pixel intensity in this PoC must not be interpreted as calibrated luminance.

True photometric luminance estimation requires additional information such as camera calibration, exposure settings, sensor response characteristics and photometric calibration.

The current implementation therefore represents only relative spatial brightness and is intended as a methodological prototype rather than a photometrically calibrated ELF implementation.

## Project Structure

```text
fisheye-sky-brightness-poc/
│
├── data/
│   └── fisheye_sky.jpg
│
├── output/
│
├── main.py
├── requirements.txt
└── README.md
```

## Installation

Create a Python environment and install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Place a fisheye sky image in:

```text
data/fisheye_sky.jpg
```

Then run:

```bash
python main.py
```

The generated figures will be stored in the `output` directory.

## Possible Extensions

Future extensions could include:

- automatic detection of the fisheye image boundary,
- conversion from image radius to zenith angle based on the camera projection model,
- explicit azimuth and zenith-angle mapping,
- calibrated luminance estimation,
- RGB or spectral analysis,
- analysis of multiple images as a time series,
- comparison of sunrise light-field evolution,
- integration of meteorological data such as cloud cover and humidity,
- comparison with an existing Environmental Light Field implementation.

## Motivation

The project serves as a small technical preparation for research involving Environmental Light Field analysis, fisheye imaging, daylight measurements and spatiotemporal environmental data analysis.
