import { Button, ButtonProps } from "../ui/button";

interface TrackedButtonProps extends ButtonProps {
  marketName?: string;
  eventName?: string;
  eventParams?: Record<string, any>;
}

export default function TrackedButton(props: TrackedButtonProps) {
  const { marketName, eventParams = {}, onClick, ...rest } = props;

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    if (typeof window !== "undefined" && window.gtag) {
      window.gtag("event", "button_click", {
        market_name: marketName,
        ...eventParams,
        timestamp: new Date().toISOString(),
      });
    }
    if (onClick) {
      onClick(event);
    }
  };

  return <Button {...rest} onClick={handleClick} />;
}

declare global {
  interface Window {
    gtag: (
      command: "event",
      eventName: string,
      eventParams?: Record<string, any>
    ) => void;
  }
}
