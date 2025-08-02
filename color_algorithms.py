import cv2 as cv
import numpy as np


def find_closest_colour_perceptual(pixel_colour, texture_resized):
    """
    Find the closest colour using perceptual colour distance in multiple colour spaces
    """
    pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
    
    min_dist = float('inf')
    best_u, best_v = 0, 0
    
    for v in range(6):
        for u in range(7):
            texture_colour = tuple(texture_resized[v, u])
            
            # RGB Euclidean distance
            rgb_dist = cv.norm(np.array(pixel_rgb) - np.array(texture_colour))
            
            # LAB distance (perceptually uniform)
            pixel_lab = cv.cvtColor(np.uint8([[pixel_rgb]]), cv.COLOR_RGB2LAB)[0, 0]
            texture_lab = cv.cvtColor(np.uint8([[texture_colour]]), cv.COLOR_RGB2LAB)[0, 0]
            lab_dist = cv.norm(pixel_lab - texture_lab)
            
            # Weighted combination (more balanced)
            perceptual_dist = (0.6 * lab_dist) + (0.4 * rgb_dist)
            
            if perceptual_dist < min_dist:
                min_dist = perceptual_dist
                best_u, best_v = u, v
    
    return best_u, best_v

def find_closest_colour_rgb(pixel_colour, texture_resized):
    """
    Simple RGB Euclidean distance
    """
    pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
    min_dist = float('inf')
    best_u, best_v = 0, 0
    
    for v in range(6):
        for u in range(7):
            texture_colour = tuple(texture_resized[v, u])
            dist = cv.norm(np.array(pixel_rgb) - np.array(texture_colour))
            if dist < min_dist:
                min_dist = dist
                best_u, best_v = u, v
    return best_u, best_v

def find_closest_colour_hsv(pixel_colour, texture_resized):
    """
    HSV colour space matching (better for hue)
    """
    pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
    pixel_hsv = cv.cvtColor(np.uint8([[pixel_rgb]]), cv.COLOR_RGB2HSV)[0, 0]
    
    min_dist = float('inf')
    best_u, best_v = 0, 0
    
    for v in range(6):
        for u in range(7):
            texture_colour = tuple(texture_resized[v, u])
            texture_hsv = cv.cvtColor(np.uint8([[texture_colour]]), cv.COLOR_RGB2HSV)[0, 0]
            
            # Normalize HSV components for proper distance calculation
            # H: 0-180, S: 0-255, V: 0-255
            h_dist = min(abs(float(pixel_hsv[0]) - float(texture_hsv[0])), 180 - abs(float(pixel_hsv[0]) - float(texture_hsv[0]))) / 180.0
            s_dist = abs(float(pixel_hsv[1]) - float(texture_hsv[1])) / 255.0
            v_dist = abs(float(pixel_hsv[2]) - float(texture_hsv[2])) / 255.0
            
            # Weighted HSV distance (hue is most important)
            hsv_dist = (0.5 * h_dist) + (0.25 * s_dist) + (0.25 * v_dist)
            
            if hsv_dist < min_dist:
                min_dist = hsv_dist
                best_u, best_v = u, v
    return best_u, best_v

def find_closest_colour_lab(pixel_colour, texture_resized):
    """
    LAB colour space (perceptually uniform)
    """
    pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
    pixel_lab = cv.cvtColor(np.uint8([[pixel_rgb]]), cv.COLOR_RGB2LAB)[0, 0]
    
    min_dist = float('inf')
    best_u, best_v = 0, 0
    
    for v in range(6):
        for u in range(7):
            texture_colour = tuple(texture_resized[v, u])
            texture_lab = cv.cvtColor(np.uint8([[texture_colour]]), cv.COLOR_RGB2LAB)[0, 0]
            
            # LAB distance with proper normalization
            # LAB ranges: L: 0-100, A: -128 to +127, B: -128 to +127
            l_diff = abs(float(pixel_lab[0]) - float(texture_lab[0])) / 100.0
            a_diff = abs(float(pixel_lab[1]) - float(texture_lab[1])) / 255.0
            b_diff = abs(float(pixel_lab[2]) - float(texture_lab[2])) / 255.0
            
            # Weighted LAB distance (L is most important for brightness)
            lab_dist = (0.5 * l_diff) + (0.25 * a_diff) + (0.25 * b_diff)
            
            if lab_dist < min_dist:
                min_dist = lab_dist
                best_u, best_v = u, v
    return best_u, best_v

def find_closest_colour_weighted(pixel_colour, texture_resized):
    """
    Weighted RGB with saturation boost
    """
    pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
    pixel_hsv = cv.cvtColor(np.uint8([[pixel_rgb]]), cv.COLOR_RGB2HSV)[0, 0]
    
    min_dist = float('inf')
    best_u, best_v = 0, 0
    
    for v in range(6):
        for u in range(7):
            texture_colour = tuple(texture_resized[v, u])
            texture_hsv = cv.cvtColor(np.uint8([[texture_colour]]), cv.COLOR_RGB2HSV)[0, 0]
            
            # RGB distance
            rgb_dist = cv.norm(np.array(pixel_rgb) - np.array(texture_colour))
            
            # Saturation difference (normalized)
            sat_diff = abs(float(pixel_hsv[1]) - float(texture_hsv[1])) / 255.0
            
            # Weighted distance
            total_dist = rgb_dist + (sat_diff * 100.0)  # Boost saturation importance
            
            if total_dist < min_dist:
                min_dist = total_dist
                best_u, best_v = u, v
    return best_u, best_v

def find_closest_colour_simple(pixel_colour, texture_resized):
    """
    Simple RGB with grayscale penalty
    """
    pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
    
    # Calculate saturation to avoid grays
    pixel_hsv = cv.cvtColor(np.uint8([[pixel_rgb]]), cv.COLOR_RGB2HSV)[0, 0]
    pixel_saturation = pixel_hsv[1]
    
    min_dist = float('inf')
    best_u, best_v = 0, 0
    
    for v in range(6):
        for u in range(7):
            texture_colour = tuple(texture_resized[v, u])
            texture_hsv = cv.cvtColor(np.uint8([[texture_colour]]), cv.COLOR_RGB2HSV)[0, 0]
            texture_saturation = texture_hsv[1]
            
            # RGB distance
            rgb_dist = cv.norm(np.array(pixel_rgb) - np.array(texture_colour))
            
            # Penalize matching to grays if original has colour
            if pixel_saturation > 30 and texture_saturation < 30:
                rgb_dist *= 2.0  # Heavy penalty for matching colour to gray
            
            if rgb_dist < min_dist:
                min_dist = rgb_dist
                best_u, best_v = u, v
    return best_u, best_v

def find_closest_colour_perceptual_hsv(pixel_colour, texture_resized):
    """
    Perceptual HSV matching with hue prioritization
    """
    pixel_rgb = (pixel_colour[2], pixel_colour[1], pixel_colour[0])
    
    # Convert to HSV for perceptual matching
    pixel_hsv = cv.cvtColor(np.uint8([[pixel_rgb]]), cv.COLOR_RGB2HSV)[0, 0]
    
    min_dist = float('inf')
    best_u, best_v = 0, 0
    
    for v in range(6):
        for u in range(7):
            texture_colour = tuple(texture_resized[v, u])
            texture_hsv = cv.cvtColor(np.uint8([[texture_colour]]), cv.COLOR_RGB2HSV)[0, 0]
            
            # Hue distance with wrap-around (scaled up for better sensitivity)
            hue_diff = min(abs(float(pixel_hsv[0]) - float(texture_hsv[0])), 180 - abs(float(pixel_hsv[0]) - float(texture_hsv[0]))) / 180.0
            
            # Saturation and value differences (scaled up)
            sat_diff = abs(float(pixel_hsv[1]) - float(texture_hsv[1])) / 255.0
            val_diff = abs(float(pixel_hsv[2]) - float(texture_hsv[2])) / 255.0
            
            # Weighted perceptual distance with better scaling
            total_dist = (0.6 * hue_diff * 255.0) + (0.25 * sat_diff * 255.0) + (0.15 * val_diff * 255.0)
            
            if total_dist < min_dist:
                min_dist = total_dist
                best_u, best_v = u, v
    
    return best_u, best_v

# All algs to be exported from this file
ALGORITHMS = {
    'perceptual': find_closest_colour_perceptual,
    'rgb': find_closest_colour_rgb,
    'hsv': find_closest_colour_hsv,
    'lab': find_closest_colour_lab,
    'weighted': find_closest_colour_weighted,
    'simple': find_closest_colour_simple,
    'perceptual_hsv': find_closest_colour_perceptual_hsv
}

def get_available_algorithms():
    """
    Return a list of available algorithm names
    """
    return list(ALGORITHMS.keys())

def get_algorithm_function(algorithm_name):
    """
    Get the function for a given algorithm name
    """
    return ALGORITHMS.get(algorithm_name) 