#!/usr/bin/env node
import fs from "fs";
import { randomBytes } from "crypto";
import { formatDate } from "date-fns";

const calculateLifePath = (day: string, month: string, year: string) => {
  day = day.replace(/9/, "");
  month = month.replace(/9/, "");
  year = year.replace(/9/, "");
  let sum = parseInt(day) + parseInt(month) + parseInt(year);
  while (sum > 9) {
    sum = sum
      .toString()
      .split("")
      .reduce((acc, curr) => acc + parseInt(curr), 0);
  }
  return sum;
};
const days = Array.from({ length: 31 }, (_, i) => i + 1);
const calculateThePsychicNumber = (day: number) => {
  if (!days.includes(day)) {
    throw new Error("Invalid day");
  }

  let sum = day;
  while (sum > 9) {
    sum = sum
      .toString()
      .split("")
      .reduce((acc, curr) => acc + parseInt(curr), 0);
  }
  return sum;
};

const dob = process.argv.find((arg) => arg.startsWith("--dob=")); // format: DD.MM.YYYY
const name = process.argv.find((arg) => arg.startsWith("--name="));

if (dob && name) {
  const dobValue = dob.split("=")[1];
  const nameValue = name.split("=")[1];
  const split = dobValue.split(".");
  let day = split[0];
  let month = split[1];
  let year = split[2];
  const lifePath = calculateLifePath(day, month, year);

  fs.readFile("lifepaths.json", (err, data) => {
    if (err) throw err;
    let lifepaths = JSON.parse(data as any);
    const lifePathExists = lifepaths.find(({ name }) => name === nameValue);
    if (lifePathExists) {
      throw Error("Name '" + nameValue + "' already exists", {
        cause: new Error("Name already exists"),
      });
    }
    lifepaths.push({
      id: randomBytes(16).toString("hex"),
      name: nameValue,
      lifePath: lifePath,
      dob: dobValue,
      formattedDob: formatDate(new Date(dobValue), "dd.MM.yyyy"),
    });
    fs.writeFile(
      "lifepaths.json",
      JSON.stringify(lifepaths, null, 2),
      (err) => {
        if (err) throw err;
      }
    );
  });
}
