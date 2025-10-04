import { motion } from 'framer-motion';
import { ReactNode } from 'react';

export default function AnimatedBlock({ children, delay = 0 }: { children: ReactNode; delay?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-20%' }}
      transition={{ duration: 0.4, delay: delay * 0.5, ease: [0.21, 1.03, 0.27, 1] }}
    >
      {children}
    </motion.div>
  );
}
