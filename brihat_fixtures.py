"""Brihat comparison data transcribed from screenshots (handoff sections 7-8).
COMPARISON FIXTURES, not astronomical ground truth. Displayed DMS is rounded to 1 arcsec."""

CASE_C = {
 "label": "CASE C", "date": "1985-12-21", "time": "14:40:00", "place": "Patna",
 "planets": {
  "Ascendant": ("030:42:20","Ve","Su","Ra","Ve"),
  "Sun":       ("245:53:26","Ju","Ke","Ra","Ju"),
  "Moon":      ("001:15:05","Ma","Ke","Ve","Su"),
  "Mars":      ("190:30:30","Ve","Ra","Sa","Sa"),
  "Mercury":   ("224:59:27","Ma","Sa","Ju","Ju"),
  "Jupiter":   ("292:31:37","Sa","Mo","Ve","Me"),
  "Venus":     ("238:53:15","Ma","Me","Sa","Ve"),
  "Saturn":    ("220:27:24","Ma","Sa","Su","Ma"),
  "Rahu":      ("012:48:40","Ma","Ke","Me","Ju"),
  "Ketu":      ("192:48:40","Ve","Ra","Me","Me"),
  "Uranus":    ("235:20:32","Ma","Me","Ra","Ke"),
  "Neptune":   ("249:34:38","Ju","Ke","Sa","Sa"),
  "Pluto":     ("193:03:00","Ve","Ra","Me","Ve"),
 },
 "cusps": {
  "1":("030:42:20","Ve","Su","Ra","Ve"), "2":("057:35:17","Ve","Ma","Ju","Ma"),
  "3":("081:28:40","Me","Ju","Ju","Ma"), "4":("106:28:51","Mo","Sa","Ju","Ra"),
  "5":("136:05:02","Su","Ve","Su","Ke"), "6":("172:09:45","Me","Mo","Ve","Sa"),
  "7":("210:42:20","Ma","Ju","Ma","Ra"), "8":("237:35:17","Ma","Me","Ju","Ma"),
  "9":("261:28:40","Ju","Ve","Ju","Mo"), "10":("286:28:51","Sa","Mo","Sa","Ve"),
  "11":("316:05:02","Sa","Ra","Ve","Ra"), "12":("352:09:45","Ju","Me","Su","Ve"),
 },
}

CASE_D = {
 "label": "CASE D", "date": "2025-11-20", "time": "14:23:19", "place": "Dehradun",
 "planets": {
  "Ascendant": ("337:17:08","Ju","Sa","Me","Sa"),
  "Sun":       ("214:09:54","Ma","Sa","Sa","Ve"),
  "Moon":      ("215:06:23","Ma","Sa","Sa","Ra"),
  "Mars":      ("227:21:41","Ma","Me","Me","Su"),
  "Mercury":   ("214:12:29","Ma","Sa","Sa","Ve"),
  "Jupiter":   ("090:50:05","Mo","Ju","Ma","Sa"),
  "Venus":     ("202:43:15","Ve","Ju","Sa","Ve"),
  "Saturn":    ("331:03:49","Ju","Ju","Ma","Ke"),
  "Rahu":      ("320:14:22","Sa","Ju","Ju","Sa"),
  "Ketu":      ("140:14:22","Su","Ve","Ju","Ju"),
  "Uranus":    ("035:24:25","Ve","Su","Me","Ke"),
  "Neptune":   ("335:17:41","Ju","Sa","Sa","Ju"),
  "Pluto":     ("277:22:38","Sa","Su","Ke","Ra"),
 },
 "cusps": {
  "1":("337:17:08","Ju","Sa","Me","Sa"), "2":("015:04:50","Ma","Ve","Ve","Sa"),
  "3":("043:06:13","Ve","Mo","Ra","Ke"), "4":("066:45:38","Me","Ra","Ra","Ra"),
  "5":("090:32:30","Mo","Ju","Mo","Su"), "6":("118:58:01","Mo","Me","Sa","Ve"),
  "7":("157:17:08","Me","Su","Ke","Ma"), "8":("195:04:50","Ve","Ra","Ke","Sa"),
  "9":("223:06:13","Ma","Sa","Ra","Ra"), "10":("246:45:38","Ju","Ke","Ra","Ke"),
  "11":("270:32:30","Sa","Su","Ra","Ve"), "12":("298:58:01","Sa","Ma","Sa","Ve"),
 },
}

CASES_META_ONLY = {
 "CASE A": {"date": "1979-11-11", "time": "23:11:00", "place": "Delhi",
            "note": "reference material exists but numeric tables were not transcribed in the handoff"},
 "CASE B": {"date": "1985-12-20", "time": "12:32:40", "place": "Jaipur",
            "note": "reference material exists but numeric tables were not transcribed in the handoff"},
}
