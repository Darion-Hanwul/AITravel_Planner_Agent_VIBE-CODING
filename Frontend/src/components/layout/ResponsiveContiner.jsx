export const ResponsiveContainer = ({ children, className = "" }) => {
  return (
    <div className={`w-full flex flex-col flex-1 min-w-0 overflow-x-hidden ${className}`}>
      {children}
    </div>
  );
};

export default ResponsiveContainer;