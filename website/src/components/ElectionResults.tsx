"use client";

import { useState } from "react";
import ElectionChart from "./ElectionChart";
import BitcoinChart from "./BitcoinChart";
import WinnerChart from "./WinnerChart";
import TrackedButton from "./common/TrackedButton";
import { markets, swingStates } from "@/lib/consts";
import { Market } from "@/lib/types";

interface ElectionResultsProps {
  statesData: any[];
  nationalData: any[];
  btcData: any[];
  winnerData: any[];
}

export default function ElectionResults({
  statesData,
  nationalData,
  btcData,
  winnerData,
}: ElectionResultsProps) {
  const [visibleCharts, setVisibleCharts] = useState<{
    [key: string]: boolean;
  }>(
    markets.reduce<{ [key: string]: boolean }>((acc, market) => {
      acc[market.key] = market.defaultVisible ?? false;
      return acc;
    }, {})
  );

  const toggleChart = (market: Market) => {
    setVisibleCharts((prev) => ({ ...prev, [market.key]: !prev[market.key] }));
  };

  const getVisibleCharts = () => {
    return markets.filter((market) => visibleCharts[market.key]);
  };

  return (
    <div className="container mx-auto">
      <div className="flex flex-wrap gap-2 mb-4 max-w-2xl justify-center mx-auto">
        {markets.map((market) => (
          <TrackedButton
            key={market.key}
            onClick={() => toggleChart(market)}
            variant={visibleCharts[market.key] ? "default" : "outline"}
          >
            {market.displayText}
          </TrackedButton>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {getVisibleCharts().map((market) => (
          <>
            {market.key === "btc" && <BitcoinChart data={btcData} />}
            {market.key === "winner" && <WinnerChart data={winnerData} />}
            {market.key === "popular" && (
              <ElectionChart
                data={nationalData}
                title={market.displayText}
                marketKey="market_probability"
                voteKey="vote_pct"
                totalVotesKey="total_votes"
                totalVotesEstimatedKey="total_votes_estimated"
                isNational
              />
            )}
            {swingStates.includes(market.key) && (
              <ElectionChart
                data={statesData.filter((d) => d.state === market.key)}
                title={market.displayText}
                marketKey="market_probability"
                voteKey="vote_pct"
                totalVotesKey="total_votes"
                totalVotesEstimatedKey="total_votes_estimated"
              />
            )}
          </>
        ))}
      </div>
    </div>
  );
}
