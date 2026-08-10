export const PageContainer = ({ children, maxWidth = "max-w-7xl", className = "" }) => {
  return (
    <div className={`w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 ${maxWidth} ${className}`}>
      {children}
    </div>
  );
};

export default PageContainer;