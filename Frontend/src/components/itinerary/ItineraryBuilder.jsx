/* eslint-disable no-unused-vars */
import  { useState } from "react";
import ItineraryControls from "./ItineraryControls";
import ItineraryWeek from "./ItineraryWeek";
import AddActivityForm from "./AddActivityForm";

export const ItineraryBuilder = ({ days = [], onSave, onExportPDF }) => {
  const [showAddForm, setShowAddForm] = useState(false);

  return (
    <div className="space-y-6">
      <ItineraryControls
        onAddActivity={() => setShowAddForm(true)}
        onSave={onSave}
        onExportPDF={onExportPDF}
      />

      {showAddForm && (
        <AddActivityForm
          onAdd={(act) => {
            setShowAddForm(false);
          }}
          onCancel={() => setShowAddForm(false)}
        />
      )}

      <ItineraryWeek days={days} />
    </div>
  );
};

export default ItineraryBuilder;