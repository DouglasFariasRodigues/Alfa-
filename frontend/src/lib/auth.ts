export const auth = {
  isLoggedIn: () => !!localStorage.getItem('access_token'),
  getUserType: () => localStorage.getItem('userType'),
  getUserName: () => localStorage.getItem('userName') || 'Usuário',
  getUserEmail: () => localStorage.getItem('userEmail') || 'usuario@exemplo.com',
  getUserProfileImage: () => localStorage.getItem('userProfileImage') || '',
  setUserProfileImage: (imageUrl: string) => {
    localStorage.setItem('userProfileImage', imageUrl);
  },
  login: (userType: string, token: string, userName?: string, userEmail?: string) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('userType', userType);
    if (userName) localStorage.setItem('userName', userName);
    if (userEmail) localStorage.setItem('userEmail', userEmail);
  },
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('userType');
    localStorage.removeItem('userName');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userProfileImage');
  },
  getToken: () => localStorage.getItem('access_token'),
};
