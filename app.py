from flask import Flask, jsonify, render_template, request

from classSection import ClassSection
from preferences import ScoringPreferences
import scheduler
import scorer

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", defaults=ScoringPreferences.DEFAULTS)


@app.post("/api/schedules")
def create_schedules():
    payload = request.get_json(silent=True) or {}
    raw_sections = payload.get("sections", [])
    if not raw_sections:
        return jsonify(error="Add at least one section."), 400

    sections = []
    try:
        for item in raw_sections:
            code = item["code"].strip().upper()
            section_number = item.get("section_number", "001").strip() or "001"
            name = item.get("name", code).strip() or code
            online = bool(item.get("online"))
            days = "" if online else ",".join(item.get("days", []))
            time = "00:00-00:00" if online else f'{item["start"]}-{item["end"]}'
            if not code or (not online and (not days or not item.get("start") or not item.get("end"))):
                raise ValueError("Each in-person section needs a course code, day, start time, and end time.")
            sections.append(ClassSection(code, section_number, name, time, days, online))
        preferences = ScoringPreferences.from_dict(payload.get("preferences"))
    except (KeyError, ValueError, TypeError) as error:
        return jsonify(error=str(error)), 400

    schedules = scheduler.sort_schedules(scheduler.generate_schedules(scheduler.group_courses(sections)))
    scored = sorted(((scorer.score_schedule(schedule, preferences), schedule) for schedule in schedules),
                    key=lambda item: item[0], reverse=True)
    return jsonify(count=len(scored), schedules=[{
        "score": score,
        "sections": [{"code": s.get_code(), "section": s.get_section_number(), "name": s.get_name(),
                      "days": s.get_meeting_days(), "time": s.get_time(), "online": s.is_online()} for s in schedule]
    } for score, schedule in scored])


if __name__ == "__main__":
    app.run(debug=True)
