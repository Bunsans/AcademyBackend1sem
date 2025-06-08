from src.visual.message_phrase import MessageWrongSize


test_check_size_cases = [
    (
        "1",
        "1",
        MessageWrongSize(
            "",
            "width or height less than 5",
            "",
        ),
    ),
    (
        "1",
        "2",
        MessageWrongSize(
            "",
            "width or height less than 5",
            "width or height not odd",
        ),
    ),
    (
        "50",
        "13",
        MessageWrongSize(
            "",
            "width or height more than 49",
            "width or height not odd",
        ),
    ),
    (
        "13",
        "51",
        MessageWrongSize(
            "",
            "width or height more than 49",
            "",
        ),
    ),
    (
        "afg",
        "2",
        MessageWrongSize(
            "width or height not an int!",
            "",
            "",
        ),
    ),
    (
        "1",
        "50",
        MessageWrongSize(
            "",
            "width or height less than 5 or more than 49",
            "width or height not odd",
        ),
    ),
]


test_check_check_coordinate_cases = [
    ("1", "Vertical coordinate", False),
    ("-1", "Horizontal coordinate", "Horizontal coordinate less than 0"),
    ("14", "Vertical coordinate", "Vertical coordinate more than 13"),
    ("aboba", "Horizontal coordinate", "Horizontal coordinate not an int!"),
]
