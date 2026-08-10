import "react";
import ItineraryDay from "./ItineraryDay";

export const ItineraryWeek = ({ days = [], onDeleteActivity }) => {
  return (
    <div className="space-y-6">
      {days.map((dayData, index) => (
        <ItineraryDay
          key={index}
          dayNumber={index + 1}
          activities={dayData.activities || []}
          onDeleteActivity={onDeleteActivity}
        />
      ))}
    </div>
  );
};

export default ItineraryWeek;