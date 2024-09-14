import simplekml
from .new_left import main as VPL
from .new_Right import main as VPR
from flockwave.server.model import UAV


def download_mission_kml(kml_file: str, mission: list[float], sys_id: int) -> None:
    kml = simplekml.Kml()
    if len(mission) > 0:
        for i, cmd in enumerate(mission):
            kml.newpoint(name="{}_{}".format(sys_id, i), coords=[(cmd[0], cmd[1])])
    kml.save(kml_file)


async def main(
    selected_turn: str,
    numOfDrones: int,
    uavid: int,
    mission: list[float],
    uavs: list[UAV],
) -> bool:
    if len(mission) > 0:
        download_mission_kml(
            "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/kmls/Forward-Mission.kml",
            mission,
            uavid,
        )
        if selected_turn == "left":
            await VPL(numOfDrones, uavs)
        elif selected_turn == "right":
            await VPR(numOfDrones, uavs)

    return True
