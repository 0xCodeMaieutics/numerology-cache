import readline from "node:readline";

export const input = (question: string): Promise<string> => {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  return new Promise<string>((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
      rl.close();
    });
  });
};

export const inputIsConfirm = async (question: string) => {
  const prompt = await input(question);
  return ["y", "yes"].includes(prompt.toLowerCase());
};
