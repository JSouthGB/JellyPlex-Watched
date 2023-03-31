from src.functions import (
    logger,
    search_mapping,
)


def check_skip_logic(
    library_title,
    library_type,
    blacklist_library,
    whitelist_library,
    blacklist_library_type,
    whitelist_library_type,
    library_mapping=None,
):
    skip_reason = None
    library_other = None
    if library_mapping:
        library_other = search_mapping(library_mapping, library_title)

    skip_reason_black = check_blacklist_logic(
        library_title,
        library_type,
        blacklist_library,
        blacklist_library_type,
        library_other,
    )
    skip_reason_white = check_whitelist_logic(
        library_title,
        library_type,
        whitelist_library,
        whitelist_library_type,
        library_other,
    )

    # Combine skip reasons
    if skip_reason_black:
        skip_reason = skip_reason_black

    if skip_reason_white:
        if skip_reason:
            skip_reason = skip_reason + " and " + skip_reason_white
        else:
            skip_reason = skip_reason_white

    return skip_reason


def check_blacklist_logic(
    library_title,
    library_type,
    blacklist_library,
    blacklist_library_type,
    library_other=None,
):
    skip_reason = None
    if isinstance(library_type, (list, tuple, set)):
        for library_type_item in library_type:
            if library_type_item.lower() in blacklist_library_type:
                skip_reason = f"{library_type_item} is in blacklist_library_type"
    else:
        if library_type.lower() in blacklist_library_type:
            skip_reason = f"{library_type} is in blacklist_library_type"

    if library_title.lower() in [x.lower() for x in blacklist_library]:
        if skip_reason:
            skip_reason = (
                skip_reason + " and " + f"{library_title} is in blacklist_library"
            )
        else:
            skip_reason = f"{library_title} is in blacklist_library"

    if library_other:
        if library_other.lower() in [x.lower() for x in blacklist_library]:
            if skip_reason:
                skip_reason = (
                    skip_reason + " and " + f"{library_other} is in blacklist_library"
                )
            else:
                skip_reason = f"{library_other} is in blacklist_library"

    return skip_reason


def check_whitelist_logic(
    library_title,
    library_type,
    whitelist_library,
    whitelist_library_type,
    library_other=None,
):
    skip_reason = None
    if len(whitelist_library_type) > 0:
        if isinstance(library_type, (list, tuple, set)):
            for library_type_item in library_type:
                if library_type_item.lower() not in whitelist_library_type:
                    skip_reason = (
                        f"{library_type_item} is not in whitelist_library_type"
                    )
        else:
            if library_type.lower() not in whitelist_library_type:
                skip_reason = f"{library_type} is not in whitelist_library_type"

    # if whitelist is not empty and library is not in whitelist
    if len(whitelist_library) > 0:
        if library_other:
            if library_title.lower() not in [
                x.lower() for x in whitelist_library
            ] and library_other.lower() not in [x.lower() for x in whitelist_library]:
                if skip_reason:
                    skip_reason = (
                        skip_reason
                        + " and "
                        + f"{library_title} is not in whitelist_library"
                    )
                else:
                    skip_reason = f"{library_title} is not in whitelist_library"
        else:
            if library_title.lower() not in [x.lower() for x in whitelist_library]:
                if skip_reason:
                    skip_reason = (
                        skip_reason
                        + " and "
                        + f"{library_title} is not in whitelist_library"
                    )
                else:
                    skip_reason = f"{library_title} is not in whitelist_library"

    return skip_reason


def show_title_dict(user_list: dict):
    try:
        show_output_dict = {}

        show_output_keys = user_list.keys()
        show_output_keys = [dict(x) for x in list(show_output_keys)]
        for show_key in show_output_keys:
            for provider_key, provider_value in show_key.items():
                # Skip title
                if provider_key.lower() == "title":
                    continue
                if provider_key.lower() not in show_output_dict:
                    show_output_dict[provider_key.lower()] = []
                if provider_key.lower() == "locations":
                    for show_location in provider_value:
                        show_output_dict[provider_key.lower()].append(show_location)
                else:
                    show_output_dict[provider_key.lower()].append(
                        provider_value.lower()
                    )

        return show_output_dict
    except Exception:
        logger("Generating show_output_dict failed, skipping", 1)
        return {}


def episode_title_dict(user_list: dict):
    try:
        episode_output_dict = {}
        for show in user_list:
            for season in user_list[show]:
                for episode in user_list[show][season]:
                    for episode_key, episode_value in episode.items():
                        if episode_key != "status":
                            if episode_key.lower() not in episode_output_dict:
                                episode_output_dict[episode_key.lower()] = []

                        if "completed" not in episode_output_dict:
                            episode_output_dict["completed"] = []
                        if "time" not in episode_output_dict:
                            episode_output_dict["time"] = []

                        if episode_key == "locations":
                            for episode_location in episode_value:
                                episode_output_dict[episode_key.lower()].append(
                                    episode_location
                                )
                        elif episode_key == "status":
                            episode_output_dict["completed"].append(
                                episode_value["completed"]
                            )
                            episode_output_dict["time"].append(episode_value["time"])
                        else:
                            episode_output_dict[episode_key.lower()].append(
                                episode_value.lower()
                            )

        return episode_output_dict
    except Exception:
        logger("Generating episode_output_dict failed, skipping", 1)
        return {}


def movies_title_dict(user_list: dict):
    try:
        movies_output_dict = {}
        for movie in user_list:
            for movie_key, movie_value in movie.items():
                if movie_key != "status":
                    if movie_key.lower() not in movies_output_dict:
                        movies_output_dict[movie_key.lower()] = []

                if "completed" not in movies_output_dict:
                    movies_output_dict["completed"] = []
                if "time" not in movies_output_dict:
                    movies_output_dict["time"] = []

                if movie_key == "locations":
                    for movie_location in movie_value:
                        movies_output_dict[movie_key.lower()].append(movie_location)
                elif movie_key == "status":
                    movies_output_dict["completed"].append(movie_value["completed"])
                    movies_output_dict["time"].append(movie_value["time"])
                else:
                    movies_output_dict[movie_key.lower()].append(movie_value.lower())

        return movies_output_dict
    except Exception:
        logger("Generating movies_output_dict failed, skipping", 1)
        return {}


def generate_library_guids_dict(user_list: dict):
    # Handle the case where user_list is empty or does not contain the expected keys and values
    if not user_list:
        return {}, {}, {}

    show_output_dict = show_title_dict(user_list)
    episode_output_dict = episode_title_dict(user_list)
    movies_output_dict = movies_title_dict(user_list)

    return show_output_dict, episode_output_dict, movies_output_dict
