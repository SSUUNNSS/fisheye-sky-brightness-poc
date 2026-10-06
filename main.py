import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


IMAGE_PATH = "data/fisheye_sky.jpg"
OUTPUT_DIR = "output"

N_SECTORS = 36
N_RINGS = 5
FISHEYE_RADIUS_FACTOR = 0.48


def load_image(path):
    image = cv2.imread(path)

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {path}"
        )

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image_rgb, gray


def create_polar_coordinates(gray):
    height, width = gray.shape

    cx = width / 2
    cy = height / 2

    y, x = np.indices((height, width))

    dx = x - cx
    dy = cy - y

    radius = np.sqrt(dx ** 2 + dy ** 2)

    theta = np.arctan2(dy, dx)
    theta = np.mod(theta, 2 * np.pi)

    return radius, theta


def create_fisheye_mask(gray, radius):
    height, width = gray.shape

    fisheye_radius = min(height, width) * FISHEYE_RADIUS_FACTOR

    mask = radius <= fisheye_radius

    return mask, fisheye_radius


def calculate_sector_brightness(
    gray,
    mask,
    theta
):
    sector_edges = np.linspace(
        0,
        2 * np.pi,
        N_SECTORS + 1
    )

    brightness = []

    for i in range(N_SECTORS):
        sector_mask = (
            mask
            & (theta >= sector_edges[i])
            & (theta < sector_edges[i + 1])
        )

        values = gray[sector_mask]

        if len(values) > 0:
            brightness.append(values.mean())
        else:
            brightness.append(np.nan)

    sector_centers = (
        sector_edges[:-1] + sector_edges[1:]
    ) / 2

    return sector_centers, np.array(brightness)


def calculate_spatial_matrix(
    gray,
    mask,
    radius,
    theta,
    fisheye_radius
):
    sector_edges = np.linspace(
        0,
        2 * np.pi,
        N_SECTORS + 1
    )

    ring_edges = np.linspace(
        0,
        fisheye_radius,
        N_RINGS + 1
    )

    spatial_matrix = np.full(
        (N_RINGS, N_SECTORS),
        np.nan
    )

    for ring_idx in range(N_RINGS):
        for sector_idx in range(N_SECTORS):

            region_mask = (
                mask
                & (radius >= ring_edges[ring_idx])
                & (radius < ring_edges[ring_idx + 1])
                & (theta >= sector_edges[sector_idx])
                & (theta < sector_edges[sector_idx + 1])
            )

            values = gray[region_mask]

            if len(values) > 0:
                spatial_matrix[
                    ring_idx,
                    sector_idx
                ] = values.mean()

    return spatial_matrix


def plot_original(image_rgb):
    plt.figure(figsize=(7, 7))

    plt.imshow(image_rgb)

    plt.title(
        "Original Fisheye Sky Image"
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "01_original_image.png"
        ),
        dpi=200
    )

    plt.show()


def plot_masked_brightness(
    gray,
    mask
):
    masked_gray = np.where(
        mask,
        gray,
        np.nan
    )

    plt.figure(figsize=(7, 7))

    plt.imshow(
        masked_gray
    )

    plt.colorbar(
        label="Pixel intensity"
    )

    plt.title(
        "Relative Spatial Brightness Distribution"
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "02_brightness_distribution.png"
        ),
        dpi=200
    )

    plt.show()


def plot_polar_brightness(
    sector_centers,
    brightness
):
    plt.figure(figsize=(8, 8))

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.plot(
        sector_centers,
        brightness,
        marker="o"
    )

    ax.set_title(
        "Mean Relative Brightness by Direction",
        pad=20
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "03_polar_brightness.png"
        ),
        dpi=200
    )

    plt.show()


def plot_spatial_matrix(
    spatial_matrix
):
    plt.figure(figsize=(12, 5))

    plt.imshow(
        spatial_matrix,
        aspect="auto",
        origin="lower"
    )

    plt.colorbar(
        label="Mean pixel intensity"
    )

    plt.xlabel(
        "Azimuth sector"
    )

    plt.ylabel(
        "Radial ring"
    )

    plt.title(
        "Spatial Brightness Matrix"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "04_spatial_matrix.png"
        ),
        dpi=200
    )

    plt.show()


def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    image_rgb, gray = load_image(
        IMAGE_PATH
    )

    radius, theta = (
        create_polar_coordinates(
            gray
        )
    )

    mask, fisheye_radius = (
        create_fisheye_mask(
            gray,
            radius
        )
    )

    sector_centers, brightness = (
        calculate_sector_brightness(
            gray,
            mask,
            theta
        )
    )

    spatial_matrix = (
        calculate_spatial_matrix(
            gray,
            mask,
            radius,
            theta,
            fisheye_radius
        )
    )

    plot_original(
        image_rgb
    )

    plot_masked_brightness(
        gray,
        mask
    )

    plot_polar_brightness(
        sector_centers,
        brightness
    )

    plot_spatial_matrix(
        spatial_matrix
    )

    print(
        "Analysis completed successfully."
    )

    print(
        f"Results saved in: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()