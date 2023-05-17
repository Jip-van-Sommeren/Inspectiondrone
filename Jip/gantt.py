import datetime as dt
import logging
import random
import re

import matplotlib.axes as axes
import matplotlib.container as container
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logging.basicConfig(level=30)


def color(row: int) -> dict:
    c_dict = {
        "AH": "#84C3F1",
        "AE": "#C4569A",
        "LT": "#6FE293",
        "GROUP": "#FFD342",
        "RS": "#3A76B9",
        "EK": "#B28953",
        "ND": "#E03D88",
        "JS": "#11A6C0",
        "MB": "#D6AE5C",
        "TM": "#719864",
        "MT": "#000000",
    }
    return c_dict[row["Resource"]]


def find_strings(text: str) -> str:
    pattern: str = r"(AH|AE|LT|GROUP|RS|ND|EK|JS|MB|TM|MT)"
    matches: list[str] = re.findall(pattern, text)
    if len(matches) > 0:
        if "GROUP" not in matches:
            x = random.randint(0, len(matches) - 1)
            return matches[x]
        else:
            return matches[0]
    else:
        return ""


def remove_colon(text: str) -> str:
    pattern: str = r":"
    result: str = re.sub(pattern, "", text)
    return result


def keep_string_from_number(text: str) -> str:
    if text is None:
        return None
    pattern: str = r"\d"
    match = re.search(pattern, text)

    if match:
        start_index: int = match.start()
        return text[start_index:]
    else:
        return None


def split_consecutive_subarrays(arr: list) -> list[list]:
    subarrays: list[list] = []
    current_subarray: list[int] = [arr[0]]

    for i in range(1, len(arr)):
        if arr[i] == current_subarray[-1] + 1:
            current_subarray.append(arr[i])
        else:
            subarrays.append(current_subarray)
            current_subarray = [arr[i]]

    subarrays.append(current_subarray)
    return subarrays


def flatten_list(nested_list: list) -> list:
    return [item for sublist in nested_list for item in sublist]


def remove_items(lst: list, items_to_remove: list) -> list:
    return [item for item in lst if item not in items_to_remove]


def clean_arrays(arr_with_sub_arr: list, comparison_arr: list) -> list:
    new_lst: list = []
    for sub_arr in comparison_arr:
        sub_arr: list = remove_items(sub_arr, flatten_list(arr_with_sub_arr))

        new_lst.append(sub_arr)
    return new_lst


def arrow_path(
    xy_dict: dict[int, tuple[float, float]],
    key: int,
    sizing: float,
    index: int,
    main_arrow: bool,
) -> path.Path:
    if main_arrow:
        return path.Path(
            [
                (xy_dict[key][0], xy_dict[key][1]),
                (xy_dict[key][0] - sizing, xy_dict[key][1]),
                (xy_dict[key][0] - sizing, xy_dict[index][1]),
                xy_dict[index],
            ]
        )
    else:
        return path.Path(
            [
                (xy_dict[key][0] - sizing, xy_dict[key][1]),
                (xy_dict[key][0] - sizing, xy_dict[index][1]),
                xy_dict[index],
            ]
        )


def draw_arrow(
    arr: list,
    xy_dict: dict[int, tuple[float, float]],
    ax: axes,
    sizing: float,
    color: str,
    main_arrow: bool,
) -> None:
    for item in arr:
        key = item[-1] + 1
        if main_arrow:
            b = patches.Circle((xy_dict[key]), radius=(sizing / 10), color="k")
            ax.add_patch(b)

        for i in item:
            a = patches.FancyArrowPatch(
                path=arrow_path(xy_dict, key, sizing, i, main_arrow),
                arrowstyle=patches.ArrowStyle.CurveB(
                    head_length=sizing * 4, head_width=sizing * 4
                ),
                connectionstyle="angle3,angleA=90,angleB=0",
                color=color,
            )

            ax.add_patch(a)


def string_split(text):
    sep = "("
    new_str = text.split(sep, 1)[0]
    return new_str


# # Set the current date as the starting date
def main() -> None:
    df: pd.DataFrame = pd.read_csv("Gantt_v2.csv", sep=";")

    df["Start_date"]: pd.Series = df["Start_date"].apply(
        lambda x: (
            (
                pd.to_datetime([x], utc=True)
                - pd.Timestamp("1970-01-01", tz="Europe/Brussels")
            )
            // pd.Timedelta("1s")
        )[0]
        if x is not None
        else x
    )
    # df["estimated end date"]: pd.Series = df["estimated end date"].apply(
    #     lambda x: (
    #         (
    #             pd.to_datetime([x], utc=True)
    #             - pd.Timestamp("1970-01-01", tz="Europe/Brussels")
    #         )
    #         // pd.Timedelta("1s")
    #     )[0]
    #     if x is not None
    #     else x
    # )

    # df["Resource"]: pd.Series = df["name"].apply(find_strings)
    # df: pd.DataFrame = df[df["Resource"] != ""]
    # print(df["Resource"])
    df: pd.DataFrame = df[["Start_date", "Task_id", "Task_desc", "Duration"]]

    df["Start_date"]: pd.Series = pd.to_datetime(df["Start_date"], unit="s")
    # print(df["Start_date"])
    # print(df["Duration"])
    df["Hours"] = df["Duration"].astype(str)
    df["randNumCol"] = np.random.randint(3, 10, df.shape[0])
    df["Duration"] = (df["Duration"] / 8) / df["randNumCol"]
    proj_start: dt.datetime = dt.datetime(2023, 4, 24)

    # number of days from project start to task start
    df["start_num"]: pd.Series = df["Start_date"] - proj_start
    logging.info(df["start_num"].dt.days + df["Duration"])
    # number of days from project start to end of tasks
    df["end_num"]: pd.Series = df["start_num"].dt.days + df["Duration"]
    logging.info(df["start_num"].max())
    # days between start and end of each task
    df["days_start_to_end"]: pd.Series = df["end_num"] - df["start_num"].dt.days
    # print(df["start_num"])
    # df["seconds_start_to_end"]: pd.Series = (
    #     df["end_num"].dt.seconds - df["start_num"].dt.seconds
    # )
    df["total_delta"]: pd.Series = df["Duration"]
    logging.info(df["total_delta"])
    # df["color"] = df.apply(color, axis=1)
    df["color"]: pd.Series = "#FFC0CB"
    df: pd.DataFrame = df.iloc[::-1].reset_index(drop=True)
    _, ax = plt.subplots(1, figsize=(20, 50))

    ax.grid()

    df["Task_desc"] = df["Task_desc"].apply(string_split)
    df["name"] = df[["Task_id", "Task_desc", "Hours"]].agg(" ".join, axis=1) + "h"
    # print(df["name"])

    df["code"]: pd.Series = df["Task_id"].str.split().str[0].apply(remove_colon)
    df["keycode"]: pd.Series = df["code"].str.split("-").str[0]
    df["subcode"]: pd.Series = (
        df["code"]
        .str.split("-")
        .str[1]
        .apply(lambda x: None if type(x) is float else x)
    )
    df["subsubcode"]: pd.Series = df["subcode"].apply(keep_string_from_number)
    df["subsubsubcode"]: pd.Series = (
        df["subsubcode"]
        .str.split(".")
        .str[1]
        .apply(lambda x: None if type(x) is float else x)
    )
    arr1: list[list[int]] = split_consecutive_subarrays(
        df[df["subsubsubcode"].notna()].index.tolist()
    )

    arr2: list[list[int]] = split_consecutive_subarrays(
        df[df["subsubcode"].notna()].index.tolist()
    )

    arr3: list[list[int]] = split_consecutive_subarrays(
        df[df["subcode"].notna()].index.tolist()
    )
    df["start_days"] = df["start_num"].dt.days
    for sub_arr in arr3:
        # print(sub_arr[0], sub_arr[-1])
        df_ = df[sub_arr[0] : sub_arr[-1] + 2]
        max_date = df_["end_num"].max()
        print(df["Task_id"][sub_arr[-1] + 1])
        df["total_delta"][sub_arr[-1] + 1] = (
            max_date - df["start_days"][sub_arr[-1] + 1]
        )
    for sub_arr in arr2:
        # print(sub_arr[0], sub_arr[-1])
        df_ = df[sub_arr[0] : sub_arr[-1] + 2]
        max_date = df_["end_num"].max()
        print(df["Task_id"][sub_arr[-1] + 1])
        df["total_delta"][sub_arr[-1] + 1] = (
            max_date - df["start_days"][sub_arr[-1] + 1]
        )
    for sub_arr in arr1:
        # print(sub_arr[0], sub_arr[-1])
        df_ = df[sub_arr[0] : sub_arr[-1] + 2]
        max_date = df_["end_num"].max()
        print(df["Task_id"][sub_arr[-1] + 1])
        df["total_delta"][sub_arr[-1] + 1] = (
            max_date - df["start_days"][sub_arr[-1] + 1]
        )
        # print(max_date - df["start_days"][sub_arr[-1] + 1])
        # print(max_date)
        # print(df_["end_num"])

    arr2: list[list[int]] = clean_arrays(arr1, arr2)

    arr3: list[list[int]] = clean_arrays(arr1 + arr2, arr3)

    xy_dict: dict[int, tuple[float, float]] = {}
    br: container.BarContainer = ax.barh(
        df["name"],
        df["total_delta"],
        left=df["start_num"].dt.days,
        color=df["color"],
        alpha=0.5,
    )
    for index, b in enumerate(br):
        xy_dict[index] = (b.get_x() - 0.25, b.get_y() + 0.4)

    style_arr: list[dict[str:list, str:float, str:str, str:bool]] = [
        {"array_name": arr1, "sizing": 0.5, "color": "r", "main_arrow": False},
        {"array_name": arr2, "sizing": 0.75, "color": "b", "main_arrow": False},
        {"array_name": arr3, "sizing": 1.0, "color": "k", "main_arrow": True},
    ]
    for style_dict in style_arr:
        draw_arrow(
            style_dict["array_name"],
            xy_dict,
            ax,
            sizing=style_dict["sizing"],
            color=style_dict["color"],
            main_arrow=style_dict["main_arrow"],
        )
    # draw_arrow(arr2, xy_dict, ax, sizing=0.67, color="b", main_arrow=False)
    # draw_arrow(arr3, xy_dict, ax, sizing=1.0, color="k", main_arrow=True)
    ##### LEGENDS #####

    # legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
    # legend_elements = [Patch(facecolor="#F8C8DC", label=i) for i in c_dict]
    # plt.legend(handles=legend_elements)
    ##### TICKS #####
    xticks: np.ndarray = np.arange(0, int(df["end_num"].max()) + 1, 3)
    logging.info(len(xticks))
    xticks_labels: pd.Index = pd.date_range(
        proj_start, end=dt.datetime(2023, 6, 30)
    ).strftime("%m/%d")
    xticks_minor: np.ndarray = np.arange(0, int(df["end_num"].max()) + 1, 1)
    logging.info(len(xticks_labels))
    ax.set_xticks(xticks)
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_xticklabels(xticks_labels[::3])
    ax.tick_params(axis="x", bottom=True, top=True, labelbottom=True, labeltop=True)
    ax.set_axisbelow(True)
    deadline_dict: dict[str : dt.timedelta] = {
        "Project Plan": ((pd.Timestamp("2023-04-28") - proj_start).days),
        "Baseline Report": ((pd.Timestamp("2023-05-04") - proj_start).days),
        "Baseline Review": ((pd.Timestamp("2023-05-09") - proj_start).days),
        "Midterm Report": ((pd.Timestamp("2023-05-26") - proj_start).days),
        "Midterm Review": ((pd.Timestamp("2023-05-30") - proj_start).days),
        "Final Report": ((pd.Timestamp("2023-06-21") - proj_start).days),
        "Final Review": ((pd.Timestamp("2023-06-26") - proj_start).days),
        "Symposium": ((pd.Timestamp("2023-06-29") - proj_start).days),
    }
    for item in deadline_dict.items():
        plt.axvline(
            x=item[1],
            label="axvline - full height",
            color="black",
            linestyle="dashed",
        )
        plt.text(
            item[1],
            140,
            item[0],
            rotation=90,
            verticalalignment="center",
        )

    plt.title("Gantt chart")
    plt.savefig("Gantt_v2_.pdf", bbox_inches="tight")
    # plt.show()


if __name__ == "__main__":
    main()
