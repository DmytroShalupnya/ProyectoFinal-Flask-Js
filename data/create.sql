CREATE TABLE "movements" (
	"datetime"	TEXT NOT NULL,
	"coin_from"	TEXT NOT NULL,
	"amount_from"	TEXT NOT NULL,
	"coin_to"	TEXT NOT NULL,
	"amount_to"	TEXT NOT NULL,
	"price_per_unit"	TEXT NOT NULL,
	PRIMARY KEY("datetime")
);

CREATE TABLE "wallet" (
	"coin"	TEXT NOT NULL UNIQUE,
	"amount"	TEXT,
	PRIMARY KEY("coin")
);