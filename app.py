
from flask import Flask,  request, jsonify
import json




app = Flask(__name__)

@app.route('/api/Status update', methods=['POST'])
def status_update():
    try:
        data = request.get_json()
        print("📥 נתונים שהתקבלו:", data)  # הדפסה לבדיקה
        # עיבוד הנתונים כאן...
        return jsonify({"message": "Success"}), 200
    except Exception as e:
        print("❌ שגיאה:", e)  # הדפסת שגיאה בשרת
        return jsonify({"error": str(e)}), 500


def status_update(macAddress,status):
 try:
     with open(f"{macAddress}_status.json","w" ,encoding='utf-8') as f:
        json.dump(status, f, ensure_ascii=False, indent=4)
     return jsonify({"message": "Data saved successfully!"}), 200
 except Exception as e:
     return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
 app.run(debug=True)

