export default function Hero() {
  return (
    <>
      <h1 className="text-3xl font-bold text-center font-mono">election.dev</h1>

      <p className="text-center pt-2 pb-4 max-w-xl justify-self-center">
        Historical analysis of market developments during the 2024 presidential
        election. The data is collected from the NYT, Polymarket, and Binance.
        Verify the methodology{" "}
        <a
          href="https://github.com/0xmanny/election-dev"
          target="_blank"
          className="hover:underline text-blue-800 font-semibold"
        >
          here
        </a>
        .
      </p>
    </>
  );
}
