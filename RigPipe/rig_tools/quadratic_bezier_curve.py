import maya.cmds as cmds


def quadratic_bezier_curve(points, t):
    # Extract coordinates of the control points
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    z_coords = [point[2] for point in points]

    # Calculate the parametric equations for x, y, and z
    x = (1 - t) ** 4 * x_coords[0] + 4 * (1 - t) ** 3 * t * x_coords[1] + 6 * (1 - t) ** 2 * t ** 2 * x_coords[
        2] + 4 * (1 - t) * t ** 3 * x_coords[3] + t ** 4 * x_coords[4]
    y = (1 - t) ** 4 * y_coords[0] + 4 * (1 - t) ** 3 * t * y_coords[1] + 6 * (1 - t) ** 2 * t ** 2 * y_coords[
        2] + 4 * (1 - t) * t ** 3 * y_coords[3] + t ** 4 * y_coords[4]
    z = (1 - t) ** 4 * z_coords[0] + 4 * (1 - t) ** 3 * t * z_coords[1] + 6 * (1 - t) ** 2 * t ** 2 * z_coords[
        2] + 4 * (1 - t) * t ** 3 * z_coords[3] + t ** 4 * z_coords[4]

    # Return the point on the curve
    return (x, y, z)


# Define control points
points = [(0, 0, 0), (0, 5, 0), (0, 5.2, 0), (-0.2, 5.2, 0), (-2, 0, 0)]

# Create locators to visualize control points
for i, point in enumerate(points):
    locator_name = 'locator_{}'.format(i)
    locator = cmds.spaceLocator(name=locator_name)[0]
    cmds.move(point[0], point[1], point[2], locator)

# Calculate equally spaced points along the curve
num_points = 10
for i in range(num_points):
    t = float(i) / (num_points - 1)  # Calculate parameter t

    # Calculate point on the curve
    result = quadratic_bezier_curve(points, t)

    # Create locator for the point on the curve
    locator_name = 'locator_curve_{:02d}'.format(i)
    locator = cmds.spaceLocator(name=locator_name)[0]
    cmds.move(result[0], result[1], result[2], locator)

# Select all locators
cmds.select(['locator_{}'.format(i) for i in range(len(points))] + ['locator_curve_{:02d}'.format(i) for i in
                                                                    range(num_points)])