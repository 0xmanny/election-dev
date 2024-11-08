import { useMemo } from "react";
import {
  Line,
  LineChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { ChartContainer, ChartTooltipContent } from "@/components/ui/chart";
import ChartCard from "./common/ChartCard";

interface ElectionData {
  timestamp: number;
  [key: string]: number | string;
}

interface ChartDataPoint {
  timestamp: number;
  datetime: string;
  marketProbability: number;
  votePct: number;
  remainingPct: number;
}

interface ElectionChartProps {
  data: ElectionData[];
  title: string;
  marketKey: string;
  totalVotesKey: string;
  totalVotesEstimatedKey: string;
  voteKey: string;
  isNational?: boolean;
}

export default function ElectionChart({
  data,
  title,
  marketKey,
  voteKey,
  totalVotesKey,
  totalVotesEstimatedKey,
  isNational = false,
}: ElectionChartProps) {
  const chartData = useMemo<ChartDataPoint[]>(() => {
    return data.map((d) => ({
      timestamp: d.timestamp,
      datetime: new Date(d.timestamp * 1000).toLocaleString(undefined, {
        month: "numeric",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      }),
      marketProbability: Number(d[marketKey]) || 0,
      votePct: Number(d[voteKey]) || 0,
      remainingPct: Math.max(
        0,
        Number(d[totalVotesKey]) / Number(d[totalVotesEstimatedKey])
      ),
    }));
  }, [data, marketKey, voteKey, totalVotesKey, totalVotesEstimatedKey]);

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
      <div className={"flex"}>
        <ChartContainer
          config={{
            marketProbability: {
              label: "Market Probability",
              color: "#6b21a8",
            },
            votePct: {
              label: "Pct Trump",
              color: "#b35d5d",
            },
            remainingPct: {
              label: "Pct of Total Votes",
              color: "#60799c",
            },
          }}
          className="h-full w-full bg-card rounded-lg "
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
              <Legend
                verticalAlign="top"
                height={36}
                wrapperStyle={{
                  paddingBottom: "20px",
                }}
              />
              <Line
                type="monotone"
                dataKey="marketProbability"
                stroke="#6b21a8"
                name="Market Probability"
                dot={false}
                activeDot={{ r: 4 }}
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="votePct"
                name="Pct Trump"
                stroke="#b35d5d"
                dot={false}
                activeDot={{ r: 4 }}
                strokeWidth={2}
              />
              {!isNational && (
                <Line
                  type="monotone"
                  dataKey="remainingPct"
                  stroke="#60799c"
                  name="Pct Total Votes"
                  dot={false}
                  activeDot={{ r: 4 }}
                  strokeWidth={2}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </div>
    </ChartCard>
  );
}
