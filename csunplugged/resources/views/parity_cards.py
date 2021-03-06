"""Module for generating Parity Cards resource."""

from PIL import Image, ImageDraw
from utils.retrieve_query_parameter import retrieve_query_parameter


def resource_image(request, resource):
    """Create a image for Parity Cards resource.

    Args:
        request: HTTP request object (HttpRequest).
        resource: Object of resource data (Resource).

    Returns:
        A list of Pillow image objects (list).
    """
    CARDS_COLUMNS = 4
    CARDS_ROWS = 5
    CARD_SIZE = 500
    IMAGE_SIZE_X = CARD_SIZE * CARDS_COLUMNS
    IMAGE_SIZE_Y = CARD_SIZE * CARDS_ROWS
    LINE_COLOUR = "#000000"
    LINE_WIDTH = 3

    front_page = Image.new("RGB", (IMAGE_SIZE_X, IMAGE_SIZE_Y), "#fff")
    draw = ImageDraw.Draw(front_page)
    for x_coord in range(0, IMAGE_SIZE_X, CARD_SIZE):
        draw.line([(x_coord, 0), (x_coord, IMAGE_SIZE_Y)], fill=LINE_COLOUR, width=LINE_WIDTH)
    draw.line([(IMAGE_SIZE_X - 1, 0), (IMAGE_SIZE_X - 1, IMAGE_SIZE_Y)], fill=LINE_COLOUR, width=LINE_WIDTH)
    for y_coord in range(0, IMAGE_SIZE_Y, CARD_SIZE):
        draw.line([(0, y_coord), (IMAGE_SIZE_X, y_coord)], fill=LINE_COLOUR, width=LINE_WIDTH)
    draw.line([(0, IMAGE_SIZE_Y - 1), (IMAGE_SIZE_X, IMAGE_SIZE_Y - 1)], fill=LINE_COLOUR, width=LINE_WIDTH)

    # Retrieve parameters
    parameter_options = valid_options()
    back_colour = retrieve_query_parameter(request, "back_colour", parameter_options["back_colour"])

    if back_colour == "black":
        back_colour_hex = "#000000"
    elif back_colour == "blue":
        back_colour_hex = "#3366ff"
    elif back_colour == "green":
        back_colour_hex = "#279f2d"
    elif back_colour == "purple":
        back_colour_hex = "#6e3896"
    else:
        back_colour_hex = "#cc0423"

    back_page = Image.new("RGB", (IMAGE_SIZE_X, IMAGE_SIZE_Y), back_colour_hex)

    return [front_page, back_page]


def subtitle(request, resource):
    """Return the subtitle string of the resource.

    Used after the resource name in the filename, and
    also on the resource image.

    Args:
        request: HTTP request object (HttpRequest).
        resource: Object of resource data (Resource).

    Returns:
        text for subtitle (str).
    """
    text = "{} back - {}".format(
        retrieve_query_parameter(request, "back_colour"),
        retrieve_query_parameter(request, "paper_size")
    )
    return text


def valid_options():
    """Provide dictionary of all valid parameters.

    This excludes the header text parameter.

    Returns:
        All valid options (dict).
    """
    return {
        "back_colour": ["black", "blue", "green", "purple", "red"],
        "paper_size": ["a4", "letter"],
    }
