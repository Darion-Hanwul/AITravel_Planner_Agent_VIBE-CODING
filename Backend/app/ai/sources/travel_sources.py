from app.ai.sources.source import Source


TRAVEL_SOURCES: list[Source] = [

    # =====================================================
    # WIKIVOYAGE
    # =====================================================

    Source(
        name="Wikivoyage Japan",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Japan",
        ],
        description="Official Wikivoyage travel guide for Japan.",
    ),

    Source(
        name="Wikivoyage South Korea",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/South_Korea",
        ],
        description="Official Wikivoyage travel guide for South Korea.",
    ),

    Source(
        name="Wikivoyage Singapore",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Singapore",
        ],
        description="Official Wikivoyage travel guide for Singapore.",
    ),

    Source(
        name="Wikivoyage Indonesia",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Indonesia",
        ],
        description="Official Wikivoyage travel guide for Indonesia.",
    ),

    Source(
        name="Wikivoyage Thailand",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Thailand",
        ],
        description="Official Wikivoyage travel guide for Thailand.",
    ),

    Source(
        name="Wikivoyage Malaysia",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Malaysia",
        ],
        description="Official Wikivoyage travel guide for Malaysia.",
    ),

    Source(
        name="Wikivoyage Vietnam",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Vietnam",
        ],
        description="Official Wikivoyage travel guide for Vietnam.",
    ),

    Source(
        name="Wikivoyage Australia",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Australia",
        ],
        description="Official Wikivoyage travel guide for Australia.",
    ),

    Source(
        name="Wikivoyage France",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/France",
        ],
        description="Official Wikivoyage travel guide for France.",
    ),

    Source(
        name="Wikivoyage Italy",
        category="travel",
        base_url="https://en.wikivoyage.org",
        urls=[
            "/wiki/Italy",
        ],
        description="Official Wikivoyage travel guide for Italy.",
    ),
]