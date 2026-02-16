import { TelegramClient } from "telegram";
import { StringSession } from "telegram/sessions";
import readline from "readline";
import { NewMessage, NewMessageEvent } from "telegram/events";

const apiId = 10956167;
const apiHash = "a8c9c00407e2b74b23fdc72596ae6d87";
const stringSession = new StringSession("1BAAOMTQ5LjE1NC4xNjcuOTEAUEqyKvB+JhxocVK3VaPRzr46MVu5LvpX7qDhg1Q57p/sUYmnZQ2UE0VMxLtECqZ5BuqjJg8VRDC1gRNldGW62uc3Vuz3KNCpVurypjx19KIoPl3JLD6b7idcgtaJ2G4gRR97wecZ/6wnIys2fxUIObqbxLmy7dED+g2KfB5MBY2tvAaMonTPrLr9WjXuFJi7eIKPzGrRd31ctwSbIJlaBe4G9G9TTw2zwnrZ666ybOUeDCJXAdp2HY89HGqrLdWVNvZVjttD5t6fUD52mlYoyMmiM84SZp3MwT4BPMxgTNOPxot8xBrf4/XGzZvmE2VNpUOQ8yPwyidlrjNohdl8vpg="); // fill this later with the value from session.save()


const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});


(async () => {
  console.log("Loading interactive example...");
  const client = new TelegramClient(stringSession, apiId, apiHash, {
    connectionRetries: 5,
  });
  await client.start({
    phoneNumber: async () =>
      new Promise((resolve) =>
        rl.question("Please enter your number: ", resolve)
      ),
    password: async () =>
      new Promise((resolve) =>
        rl.question("Please enter your password: ", resolve)
      ),
    phoneCode: async () =>
      new Promise((resolve) =>
        rl.question("Please enter the code you received: ", resolve)
      ),
    onError: (err) => console.log(err),
  });
  console.log("You should now be connected.");
  console.log(client.session.save()); // Save this string to avoid logging in again
  client.addEventHandler(async (update: NewMessageEvent) => {
    const text = update.message.text;
    const start = new Date()
    for (let i = 0; i < 1_000_000_000; i++) {
      let j = 0;
    }
    const end = new Date()
    console.log(end.getTime() - start.getTime())
    await update.message.respond({
      message: text
    });
  }, new NewMessage({
    fromUsers: [ "ExitLagGaming" ]
  }));

})();