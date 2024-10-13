// "use client"
// import { createContext, useContext, useState } from 'react';

// // Create the loading context
// const LoadingContext = createContext();

// const useLoading = () => {
//   const context = useContext(LoadingContext);

//   // Ensure that the hook is used within a LoadingProvider
//   if (!context) {
//     throw new Error('useLoading must be used within a LoadingProvider');
//   }

//   return context;
// };


// // LoadingProvider component to wrap the entire app
// const LoadingProvider = ({ children }) => {
//   const [isLoading, setIsLoading] = useState(false);

//   return (
//     <div>
//     <LoadingContext.Provider value={{ isLoading, setIsLoading }}>
//       {children}
//     </LoadingContext.Provider>
//     </div>
//   );
// };

// export {useLoading, LoadingProvider}