import { promises as fs } from "fs";
import path from "path";
import ElectionResults from "@/components/ElectionResults";
import Hero from "@/components/Hero";

export default async function Home() {
  const statesDataPath = path.join(
    process.cwd(),
    "public/data/state_results.json"
  );
  const nationalDataPath = path.join(
    process.cwd(),
    "public/data/national_results.json"
  );
  const btcDataPath = path.join(process.cwd(), "public/data/btc_data.json");
  const winnerDataPath = path.join(
    process.cwd(),
    "public/data/winner_results.json"
  );

  const statesData = JSON.parse(await fs.readFile(statesDataPath, "utf8"));
  const nationalData = JSON.parse(await fs.readFile(nationalDataPath, "utf8"));
  const btcData = JSON.parse(await fs.readFile(btcDataPath, "utf8"));
  const winnerData = JSON.parse(await fs.readFile(winnerDataPath, "utf8"));

  return (
    <div>
      <Hero />
      <ElectionResults
        statesData={statesData}
        nationalData={nationalData}
        winnerData={winnerData}
        btcData={btcData}
      />
    </div>
  );
}
