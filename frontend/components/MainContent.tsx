const MainContent = ({ children }: { children: React.ReactNode }) => {
    return (
      <main className="flex flex-1 flex-col gap-4 p-2 lg:gap-4 lg:p-4">
        {children}
      </main>
    );
  };
  
  export default MainContent;
  