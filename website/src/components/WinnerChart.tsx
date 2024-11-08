"use client";

import { useMemo } from "react";
import {
  Line,
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { ChartContainer, ChartTooltipContent } from "@/components/ui/chart";
import ChartCard from "./common/ChartCard";

interface MarketData {
  timestamp: number;
  market: string;
  probability: number;
}

interface MarketProbabilityChartProps {
  data: MarketData[];
  title?: string;
}

export default function MarketProbabilityChart({
  data,
  title = "Trump Victory Probability",
}: MarketProbabilityChartProps) {
  const chartData = useMemo(() => {
    return data.map((d) => ({
      timestamp: d.timestamp,
      datetime: new Date(d.timestamp * 1000).toLocaleString(undefined, {
        month: "numeric",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      }),
      probability: d.probability,
    }));
  }, [data]);

  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[250px] bg-muted/10 rounded-lg">
        <p className="text-muted-foreground">
          No data available for this chart.
        </p>
      </div>
    );
  }

  return (
    <ChartCard title={title}>
      <ChartContainer
        config={{
          probability: {
            label: "Probability",
            color: "#6b21a8",
          },
        }}
        className="h-full w-full bg-card rounded-lg"
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ bottom: 7 }}
            syncId="syncCharts"
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="hsl(var(--border))"
              opacity={0.4}
            />
            <XAxis
              dataKey="datetime"
              angle={-45}
              textAnchor="end"
              height={60}
              tick={{
                fontSize: 11,
                fill: "hsl(var(--foreground))",
              }}
              tickMargin={5}
            />
            <YAxis
              tick={{
                fontSize: 11,
                fill: "hsl(var(--foreground))",
              }}
              tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
              domain={[0, 1]}
            />
            <Tooltip
              content={({ active, payload, label }) => (
                <ChartTooltipContent
                  active={active}
                  payload={payload?.map((item) => ({
                    ...item,
                    value: `${(Number(item.value) * 100).toFixed(1)}%`,
                  }))}
                  label={label}
                />
              )}
              cursor={{
                stroke: "hsl(var(--muted-foreground))",
                strokeWidth: 1,
                strokeDasharray: "3 3",
              }}
            />
            <Line
              type="monotone"
              dataKey="probability"
              name={"Market Probability"}
              stroke="#6b21a8"
              dot={false}
              activeDot={{ r: 4 }}
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>
    </ChartCard>
  );
}
