import { integer, pgTable, varchar } from "drizzle-orm/pg-core";
export const celebritiesTable = pgTable("celebrities", {
  id: integer().primaryKey().generatedAlwaysAsIdentity(),
  name: varchar({ length: 64 }).notNull(),
  lifePathNumber: integer().notNull(),
  psychicNumber: integer().notNull(),
  dobFormatted: varchar().notNull(),
  birthDay: integer().notNull(),
  birthMonth: integer().notNull(),
  birthYear: integer().notNull(),
  zodiac: varchar().notNull(),
  bio: varchar(),
  image: varchar(),
  birthPlace: varchar(),
  professions: varchar(), // actor,director,producer
});

// select celeb that is born in x and has zodiac sign of y and is born on the second day of the month
// SELECT * FROM celebrities WHERE birthPlace LIKE '%x%' AND zodiac = '%y%' AND birthDay = 2;
