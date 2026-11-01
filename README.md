# David-DockIL

סקין לקודי 21, שבו כל קטגוריה בתפריט הצד היא **Dock של לשוניות**, ומתחתיו גריד של הלשונית הנבחרת.
מבוסס על [FENtastic](https://github.com/ivarbrandt/skin.fentastic) של Ivar Brandt, בגרסה של Kodi POV IL.

> **הבהרה:** פרויקט פרטי ולא רשמי. הסקין לא מכיל ולא מאחסן שום תוכן, הוא רק מציג את מה שהתוספים המותקנים אצלך מחזירים.
> הוא לא קשור ל-Kodi / XBMC Foundation, ל-POV IL, ל-Umbrella, ל-Fen Light או לעידן+, ולא מאושר על ידם.

## איפה זה עובד

| בקודי | מה מקבלים |
|---|---|
| **Kodi POV IL** | המראה של POV IL (לוגו, ברק), ותפריט: סדרות, סרטים, עידן פלוס, בגלל שראית, דף הבית |
| **כל קודי 21 עם Umbrella או Fen Light** | סדרות וסרטים מהתוסף המותקן, עם הלוגו של קודי והרקע של הסקין |
| **עם עידן+** | לשוניות עידן פלוס: ערוצים חיים, המשך צפייה, מועדפים, VOD, ערוצי גיבוי |

קטגוריה או לשונית שהתוסף שלה לא מותקן מוסתרת לבד. נבדק על Mi Box S (אנדרואיד TV). **על ווינדוס ועל מק לא נבדק.**

## התקנה מתוך קודי

1. **הגדרות > מערכת > הרחבות**: להפעיל **מקורות לא ידועים**.
2. **הגדרות > מנהל קבצים > הוסף מקור**: `https://orenddp.github.io/David-DockIL/`, ולתת לו שם, למשל `dockil`.
3. **הרחבות > התקנה מקובץ ZIP > dockil >** `repository.dockil-1.0.0.zip`.
4. **הרחבות > התקנה ממאגר > David-DockIL repository > סקינים > David-DockIL > התקן**.
   קודי מתקין איתו גם את התוסף הנלווה ואת העוזר של FENtastic.
5. כשקודי שואל אם להחליף לסקין החדש, לענות **כן**.

מאותו רגע הסקין מתעדכן לבד מהמאגר.

**ב-Kodi POV IL:** כדי שכל ההגדרות של הבילד יעבדו גם בסקין הזה (למשל OK בזמן צפייה שפותח את הנגן), סוגרים את קודי ומעתיקים
`userdata/addon_data/skin.fentastic/settings.xml` אל `userdata/addon_data/skin.david.dockil/settings.xml`.

| מערכת | התיקייה `userdata` |
|---|---|
| אנדרואיד | `Android/data/<שם החבילה של קודי>/files/.kodi/userdata/` |
| ווינדוס (לא נבדק) | `%APPDATA%\Kodi\userdata\` |
| מק (לא נבדק) | `~/Library/Application Support/Kodi/userdata/` |

כדי לחזור לסקין הקודם: **הגדרות > ממשק > סקין**.

## הגדרות סקין ← פריטי תפריט ראשי

כמו ב-FENtastic: לכל קטגוריה מתג הצג/הסתר, ו-**Set widgets**: בחירת לשונית (Widget 1–10), ואז
Move up / Move down / Display type / Rename / Remake / Remove. שורה ריקה מוסיפה לשונית מכל תוסף שמותקן.
סוגי תצוגה: Poster, BigPoster, Landscape, BigLandscape, LandscapeInfo, BigLandscapeInfo, Category.

## התוסף הנלווה (plugin.video.dockil.idanrows)

- מפצל את הערוצים החיים של עידן+ לערוצים רגילים ולערוצי גיבוי.
- "בגלל שראית" של POV, בלי הקידומת "כי צפית...".
- מתקן את "הפרק הבא" של עידן+ בתוכניות של mako, שאצלן הפרקים שמורים מהחדש לישן.
- **סנכרון "המשך צפייה" של עידן+ בין כמה מכשירים בבית** (כבוי כברירת מחדל): בהגדרות התוסף ממלאים
  **Idan Plus sync folder** עם תיקייה משותפת ברשת, למשל `smb://192.168.1.5/kodi-sync/idanplus/`, ומפעילים מחדש את קודי.
  בווינדוס 10/11 (לא נבדק) שיתוף SMB בלי סיסמה נחסם, לכן עדיף שיתוף עם משתמש וסיסמה.

## מה יש כאן

| תיקייה | מה |
|---|---|
| `src/skin.david.dockil` | הסקין |
| `src/plugin.video.dockil.idanrows` | התוסף הנלווה |
| `docs/` | מאגר הקודי (GitHub Pages) |
| `tools/` | `make_docks.py` (הלשוניות), `make_repo.py` (המאגר) |

## רישיונות וקרדיטים

- **FENtastic** של Ivar Brandt, מבוסס Estuary: GPL-2.0 (קוד) ו-CC BY-SA 4.0 (גרפיקה). הסקין הזה ממשיך באותם רישיונות.
- **העוזר של FENtastic** (`script.fentastic.helper`) של Ivar Brandt ו-Tikipeter: GPL-2.0, מופץ כאן כמו שהוא.
- **הפונט Rubik**: SIL Open Font License 1.1 (`fonts/rubik_license.txt`).
- **הרקע**: תמונה מ-Pexels, [Smooth pink and purple abstract background](https://www.pexels.com/photo/smooth-pink-and-purple-abstract-background-26770115/), ב[רישיון Pexels](https://www.pexels.com/license/).
- **הלוגו והמראה של POV IL** מופיעים רק כשהבילד Kodi POV IL מותקן, ושייכים לו.
- התוסף הנלווה: GPL-2.0.
