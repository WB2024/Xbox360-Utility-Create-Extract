def get_translations():
    """ Dictionary of UI strings for the GUI. """
    return {
        "English": {
            "title": "360 Utility Batch Create Extract v1.2",
            "author": "BY: BLAHPR 2024",
            "extract": "Extract Game Folders from ISOS",
            "create": "Create ISOS from Game Folders",
            "extract_delete": "Extract and Delete ISO Files  !!! >PERMANENTLY< !!!",
            "delete": "Delete Game Folders  !!! >PERMANENTLY< !!!",
            "fix_iso": "Fix ISO (abgx360)",
            "iso2god": "ISO to GOD (GAMES ON DEMAND)",
            "god2iso": "GOD to ISO (GAMES ON DEMAND)",
            "help": ">Help / ReadMe<",
            'help_text': (
                "* 360 Utility Batch Create Extract\n\n"
                "* Batch Extraction and Creation of Xbox 360 and Original Xbox ISOs\n\n"
                "* This setup allows you to efficiently manage multiple ISOs at once, with\n"
                "* all extracted and created files organized next to the x_ISO folder.\n\n"
                "**********************************************************************\n"
                "1.. Batch Extraction of ISOs:\n\n"
                "* Place your ISO files into folder named x_ISO.\n\n"
                "* This Utility will batch-extract games from these ISO files.\n\n"
                "* The extracted game folders will be created next to the x_ISO folder and\n"
                "* contain xex or xbe, not inside ISO folder.\n\n"
                "**********************************************************************\n"
                "2.. Batch Creation of ISOs From Game Folders:\n\n"
                "* Ensure that the game folders are placed next to the x_ISO folder, not\n"
                "* inside it.\n\n"
                "* This Utility will batch-create ISO files from these game folders that contain\n"
                "* xex or xbe.\n\n"
                "* The newly created ISO files will be saved next to the x_ISO folder.\n\n"
                "**********************************************************************\n"
                "3.. ISO to GOD:\n\n"
                "* Select an ISO file. The GOD package will be written to the chosen output folder.\n\n"
                "**********************************************************************\n"
                "4.. GOD to ISO:\n\n"
                "* Select a GOD package header file (not the .data folder).\n"
                "* The ISO will be reconstructed in the chosen output folder.\n\n"
                "**********************************************************************\n"
                "5.. Fix ISO (abgx360):\n\n"
                "* Select an ISO to verify and auto-fix with abgx360.\n"
                "* Applies AutoFix level 3 and video padding fix (-p).\n"
                "* Runs offline (-o) — no internet connection needed.\n"
                "* Use this to make newly created ISOs burnable/compatible.\n\n"
                "**********************************************************************\n"
                "* 8/19/2024 8:12 PM\n\n"
                "* BLAHPR 2024.\n\n"
                "* Contact Email: geebob273@gmail.com\n\n"
                "                                                ~~> Credits's <~~\n"
                "                                                       **********\n"
                "                     <in@fishtank.com> for your cool work and source code.\n"
            ),
        },
    }
