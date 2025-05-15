BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tournois" (
	"idTournois"	TEXT,
	"nomTournois"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("idTournois")
);
CREATE TABLE IF NOT EXISTS "equipe" (
	"numEquipe"	INTEGER,
	"nomEquipe"	TEXT NOT NULL,
	PRIMARY KEY("numEquipe")
);
CREATE TABLE IF NOT EXISTS "joueur" (
	"idJoueur"	INTEGER,
	"pseudo"	TEXT NOT NULL,
	"numEquipe"	INTEGER,
	PRIMARY KEY("idJoueur" AUTOINCREMENT),
	FOREIGN KEY("numEquipe") REFERENCES "equipe"("numEquipe")
);
CREATE TABLE IF NOT EXISTS "matchs" (
	"idMatch"	INTEGER,
	"numEquipeBleu"	INTEGER,
	"numEquipeRouge"	INTEGER,
	"numEquipeGagnante"	INTEGER,
	"statut"	TEXT,
	"dateHeure"	TEXT,
	"phase"	TEXT,
	FOREIGN KEY("numEquipeGagnante") REFERENCES "equipe"("numEquipe"),
	FOREIGN KEY("numEquipeRouge") REFERENCES "equipe"("numEquipe"),
	FOREIGN KEY("numEquipeBleu") REFERENCES "equipe"("numEquipe"),
	PRIMARY KEY("idMatch" AUTOINCREMENT)
);
INSERT INTO "tournois" VALUES ('LOL026','Le Fion de l''Invocateur','TUExkwJW');
INSERT INTO "equipe" VALUES (1,'La Fistinière');
INSERT INTO "equipe" VALUES (2,'RT pour Retard');
INSERT INTO "equipe" VALUES (3,'L''équipe de Beauvais');
INSERT INTO "equipe" VALUES (4,'T1');
INSERT INTO "joueur" VALUES (1,'Qyiana FeetSlαve#love',1);
INSERT INTO "joueur" VALUES (2,'SuckerOfBigBzez#FST',1);
INSERT INTO "joueur" VALUES (3,'Lina la sasa#FST',1);
INSERT INTO "joueur" VALUES (4,'Avalanche2Caca#FIAK',1);
INSERT INTO "joueur" VALUES (5,'T2 Goumayouslip#FST',1);
INSERT INTO "joueur" VALUES (6,'Abime Qui Crie#FST',2);
INSERT INTO "joueur" VALUES (7,'MiniZellsis#GOAT',2);
INSERT INTO "joueur" VALUES (8,'Amazoom3#1347',2);
INSERT INTO "joueur" VALUES (9,'CassouletduQ#PET',2);
INSERT INTO "joueur" VALUES (10,'Durbarode#EUW',2);
INSERT INTO "joueur" VALUES (11,'MiniEggsterr#GOAT',3);
INSERT INTO "joueur" VALUES (12,'MiniBushi#sale',3);
INSERT INTO "joueur" VALUES (13,'Pyrriclepollo#1268',3);
INSERT INTO "joueur" VALUES (14,'nomelip#EUW',3);
INSERT INTO "joueur" VALUES (15,'Arder3113#EUW',3);
INSERT INTO "joueur" VALUES (16,'Faker',4);
INSERT INTO "joueur" VALUES (17,'Doran',4);
INSERT INTO "joueur" VALUES (18,'Oner',4);
INSERT INTO "joueur" VALUES (19,'Keria',4);
INSERT INTO "joueur" VALUES (20,'Gumayusi',4);
INSERT INTO "matchs" VALUES (1,1,2,1,'terminé',NULL,'Tour 1');
INSERT INTO "matchs" VALUES (2,3,4,4,'terminé',NULL,'Tour 1');
INSERT INTO "matchs" VALUES (3,4,1,4,'terminé',NULL,'Tour 2');
COMMIT;