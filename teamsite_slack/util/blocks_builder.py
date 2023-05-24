from sf_slack.util import blocks as b
from sf_slack.util.actions import encode_action


def __add_project_section(title, projects):
    blocks = list()
    blocks.append(b.section(b.text(title)))
    for p in projects:
        t = None
        if hasattr(p, "time"):
            t = p
            p = t.project

        tracked = f" - *Tracked: {t.time}*" if t else ""

        options = [
            ("Add 0.25", encode_action(action="add", project_id=p.id, time=0.25)),
            ("Add 0.5", encode_action(action="add", project_id=p.id, time=0.5)),
            ("Add 1", encode_action(action="add", project_id=p.id, time=1)),
            ("Add 2", encode_action(action="add", project_id=p.id, time=2)),
            ("Add 3", encode_action(action="add", project_id=p.id, time=3)),
            ("Add 4", encode_action(action="add", project_id=p.id, time=4)),
            ("Subtract 1", encode_action(action="add", project_id=p.id, time=-1)),
        ]
        if t:
            options += [
                ("Reset Time", encode_action(action="set", project_id=p.id, time=0)),
                ("Delete", encode_action(action="delete", project_id=p.id)),
            ]

        blocks.append(
            b.section(
                b.text(
                    f"*<https://team.sfintra.net/project/{p.id}|{p.name}>*\n"
                    f"{p.project_code}{tracked}"
                ),
                accessory=b.dropdown("tt-track", "Track Time", options),
            )
        )
    return blocks


def show_current(results):
    tracked = results.get("tracked", [])

    blocks = []
    if len(tracked) == 0:
        blocks.append(
            b.section(b.text(f"*This week you have not tracked any time yet.*"))
        )
    else:
        total_tracked_days = sum([t.time for t in tracked])
        blocks += __add_project_section(
            f"*You have tracked {total_tracked_days} days against the "
            f"following projects this week:*",
            tracked,
        )

    resourced = results.get("resourced", [])
    if len(resourced) > 0:
        blocks.append(b.divider())
        blocks += __add_project_section(
            "*In addition you are resourced to:*", resourced
        )

    suggested = results.get("suggested", [])
    if len(suggested) > 0:
        blocks.append(b.divider())
        blocks += __add_project_section(
            "*These are other projects that may be relevant to you:*", suggested
        )

    blocks.append(
        b.section(
            b.text(
                "Use the <https://team.sfintra.net/timetracker|team site> for more options."
            )
        )
    )

    return blocks
