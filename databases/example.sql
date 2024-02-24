BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "modules" (
	"module_id"					INTEGER NOT NULL,
	"module_title"				TEXT NOT NULL,
	"module_image_url"			TEXT NOT NULL,
	"module_description"		TEXT NOT NULL,
	PRIMARY KEY("module_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "event" (
	"event_id"			INTEGER NOT NULL,
	"fk_module_id"		INTEGER NOT NULL,
	"event_date" 				TEXT NOT NULL,
	"event_title"				TEXT NOT NULL,
	"event_image_url"			TEXT NOT NULL,
	"event_description"		TEXT NOT NULL,
	PRIMARY KEY("event_id" AUTOINCREMENT),
	FOREIGN KEY("fk_module_id") REFERENCES "modules"("module_id")
);
CREATE TABLE IF NOT EXISTS "questions" (
	"question_id"			INTEGER NOT NULL,
	"fk_module_id"		INTEGER NOT NULL,
	"question" 				TEXT NOT NULL,
	"answers"				TEXT NOT NULL,
	"correct_answer"		TEXT NOT NULL,
	PRIMARY KEY("question_id" AUTOINCREMENT),
	FOREIGN KEY("fk_module_id") REFERENCES "modules"("module_id")
);
COMMIT;