import matplotlib.pyplot as plt


def plot_age_difference(data):
    colors = data["match_outcome"].map({
        1: "blue",
        0: "purple",
    })

    fig, ax = plt.subplots()

    ax.scatter(
        data["player_age"],
        data["age_diff"],
        c=colors,
    )

    ax.set_xlabel("Player Age")
    ax.set_ylabel("Age Difference")
    ax.set_title("Career Matches by Age Difference")

    return fig