# Phong Reflection Demo

This project demonstrates the Phong reflection model by simulating light reflection on a 3D ball using Python. The application utilizes graphical rendering to visualize how light interacts with the surface of the ball based on the Phong model.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Phong Reflection Model](#phong-reflection-model)
- [License](#license)

## Installation

To set up the project, ensure you have Python installed on your machine. Then, install the required dependencies by running:

```
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command in your terminal:

```
python src/main.py
```

This will open a graphical window displaying the ball with light reflection based on the Phong model.

## Phong Reflection Model

The Phong reflection model is a widely used method in computer graphics to simulate the way light reflects off surfaces. It consists of three components:

1. **Ambient Reflection**: Represents the general illumination in the scene.
2. **Diffuse Reflection**: Accounts for the light scattered in many directions when it hits a rough surface.
3. **Specular Reflection**: Models the bright spots of light that appear on shiny surfaces.

The combination of these components creates a realistic representation of how light interacts with objects in a 3D environment.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.