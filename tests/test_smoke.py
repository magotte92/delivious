import os
import py_compile
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_TRIBES = {
    "Goblin": ["Urhara", "Ortisclad"],
    "Raisen": ["Rotten", "Clarimoss"],
    "Human": ["Nazi", "Anarchist"],
    "Hyirus": ["Oram", "Slen"],
}

EXPECTED_CLASSES = {
    "Urhara": ["Warlock", "Berserker", "Thief"],
    "Ortisclad": ["Warrior", "Mage", "Shaman"],
    "Rotten": ["Necromancer", "Bone Crusher", "Shadow Shifter"],
    "Clarimoss": ["Reanimator", "Fallen Knight", "Blood Caster"],
    "Nazi": ["Sharp Shooter", "Gunsmith", "Medic"],
    "Anarchist": ["Pyromaniac", "Bruiser", "Hacker"],
    "Oram": ["Hero", "Slave", "Noble"],
    "Slen": ["Priest", "Nature Manipulator", "Dark Artist"],
}


def test_sources_compile():
    for name in ("Delivious.py", "bullet.py", "insignia.py", "test.py"):
        py_compile.compile(ROOT / name, doraise=True)


def test_race_tribe_and_class_catalog():
    import Delivious as game

    assert list(game.main_db.index) == list(EXPECTED_TRIBES)
    for race, tribes in EXPECTED_TRIBES.items():
        assert list(game.tribe_db[:][race]) == tribes
        for tribe in tribes:
            assert game.classes_db.loc[tribe, "race"] == race
            assert list(game.classes_db.loc[tribe])[1:] == EXPECTED_CLASSES[tribe]


def test_class_portraits_exist():
    import Delivious as game

    assert set(game.CLASS_ASSETS) == {
        "Berserker",
        "Mage",
        "Shaman",
        "Thief",
        "Warlock",
        "Warrior",
        "Gunsmith",
        "Sharp Shooter",
        "Noble",
        "Priest",
        "Blood Caster",
        "Bone Crusher",
        "Fallen Knight",
        "Necromancer",
        "Reanimator",
        "Shadow Shifter",
    }
    for image_path, lore_path in game.CLASS_ASSETS.values():
        assert Path(image_path).is_file(), image_path
        assert Path(lore_path).is_file() and Path(lore_path).stat().st_size > 0


def test_portrait_pipeline(tmp_path):
    import cv2
    from PIL import Image, ImageTk

    import Delivious as game

    app = game.Main()
    try:
        app.update_idletasks()
        assert set(app.frames) == {game.Login, game.CharSheet}

        image_path = next(iter(game.CLASS_ASSETS.values()))[0]
        decoded = cv2.imread(image_path)
        assert decoded is not None
        rgb = cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB)
        portrait = Image.fromarray(rgb).resize((300, 300))
        out = tmp_path / "resized.jpg"
        portrait.save(out, "JPEG", optimize=True)
        assert out.stat().st_size > 0

        photo = ImageTk.PhotoImage(portrait, master=app)
        assert photo.width() == 300
        assert photo.height() == 300
    finally:
        app.destroy()


def test_bullet_animation_accepts_frame():
    import bullet

    bullet.animate(0.1)
    x_data, y_data = bullet.redDot.get_data()
    assert list(x_data) == pytest.approx([0.1])
    assert list(y_data) == pytest.approx([np.sin(0.1)])


def test_insignia_update_appends_frame():
    import insignia

    before = len(insignia.xdata)
    insignia.update(0.5)
    assert len(insignia.xdata) == before + 1
    assert insignia.xdata[-1] == pytest.approx(0.5)


def test_cli_blank_name_exits():
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "test.py")],
        input="\n",
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=10,
        check=False,
        env=env,
    )
    assert completed.returncode == 0
    assert "Delivious" in completed.stdout or "Hey you!" in completed.stdout
    assert "Die parent" in completed.stdout
