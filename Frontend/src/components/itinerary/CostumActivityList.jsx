import "react";
import ItineraryBlock from "./ItineraryBlock";

export const CustomActivityList = ({ activities = [], onDeleteActivity }) => {
  return (
    <div className="space-y-2">
      {activities.map((act, i) => (
        <ItineraryBlock key={act.id || i} activity={act} onDelete={onDeleteActivity} />
      ))}
    </div>
  );
};

export default CustomActivityList;