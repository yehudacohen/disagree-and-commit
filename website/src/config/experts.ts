import type { Expert } from '../types';

export const EXPERTS: Expert[] = [
  {
    id: 'jeff',
    name: 'Jeff Barr',
    title: 'The Simplifier',
    color: 'orange',
    catchphrase: 'But why?',
    badge: 'Keep it Simple',
    avatarImage: '/avatars/jeff.png',
    lottieAnimations: {
      idle: '/lottie/jeff-idle.json',
      speaking: '/lottie/jeff-speaking.json',
      frustrated: {
        1: '/lottie/jeff-calm.json',
        2: '/lottie/jeff-concerned.json',
        3: '/lottie/jeff-annoyed.json',
        4: '/lottie/jeff-frustrated.json',
        5: '/lottie/jeff-steam.json'
      }
    }
  },
  {
    id: 'swami',
    name: 'Swami',
    title: 'The Shipper',
    color: 'blue',
    catchphrase: 'Just ship it!',
    badge: 'Ship It!',
    avatarImage: '/avatars/swami.png',
    lottieAnimations: {
      idle: '/lottie/swami-idle.json',
      speaking: '/lottie/swami-speaking.json',
      frustrated: {
        1: '/lottie/swami-calm.json',
        2: '/lottie/swami-concerned.json',
        3: '/lottie/swami-annoyed.json',
        4: '/lottie/swami-frustrated.json',
        5: '/lottie/swami-steam.json'
      }
    }
  },
  {
    id: 'werner',
    name: 'Werner Vogels',
    title: 'The Scale Architect',
    color: 'purple',
    catchphrase: "Won't scale!",
    badge: 'Scale or Fail',
    avatarImage: '/avatars/werner.png',
    lottieAnimations: {
      idle: '/lottie/werner-idle.json',
      speaking: '/lottie/werner-speaking.json',
      frustrated: {
        1: '/lottie/werner-calm.json',
        2: '/lottie/werner-concerned.json',
        3: '/lottie/werner-annoyed.json',
        4: '/lottie/werner-frustrated.json',
        5: '/lottie/werner-steam.json'
      }
    }
  }
];

// Helper function to get expert by ID
export function getExpertById(id: string): Expert | undefined {
  return EXPERTS.find(expert => expert.id === id);
}

// Helper function to get expert color
export function getExpertColor(expertId: string): string {
  const expert = getExpertById(expertId);
  return expert?.color || 'gray';
}

// Helper function to get expert catchphrase
export function getExpertCatchphrase(expertId: string): string {
  const expert = getExpertById(expertId);
  return expert?.catchphrase || '';
}
