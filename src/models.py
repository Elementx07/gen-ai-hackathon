"""Pydantic models for structured data extraction and validation."""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ArtisanInfo(BaseModel):
    """Artisan business information."""
    name: str = Field(description="Business or artisan name")
    story: str = Field(description="Brief story about the artisan")
    contact: str = Field(description="Email or contact information")
    address: str = Field(description="Business address")
    phone: str = Field(description="Phone number")


class Product(BaseModel):
    """Product information."""
    id: str = Field(description="Unique product identifier")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: str = Field(description="Product price")
    category: str = Field(description="Product category")
    imageUrl: str = Field(description="Product image URL path")


class GalleryItem(BaseModel):
    """Gallery item information."""
    id: str = Field(description="Unique gallery item identifier")
    name: str = Field(description="Gallery item name")
    description: str = Field(description="Gallery item description")
    imageUrl: str = Field(description="Gallery item image URL path")


class MenuItem(BaseModel):
    """Navigation menu item."""
    name: str = Field(description="Menu item name")
    href: str = Field(description="Menu item link href")
    description: str = Field(description="Menu item description")


class SocialLinks(BaseModel):
    """Social media links."""
    facebook: Optional[str] = Field(None, description="Facebook profile URL")
    instagram: Optional[str] = Field(None, description="Instagram profile URL")
    twitter: Optional[str] = Field(None, description="Twitter profile URL")
    website: Optional[str] = Field(None, description="Website URL")


class Navigation(BaseModel):
    """Navigation structure."""
    menuItems: List[MenuItem] = Field(description="Navigation menu items")
    socialLinks: SocialLinks = Field(description="Social media links")


class ColorPalette(BaseModel):
    """Color palette for design system."""
    primary: str = Field(description="Primary color")
    secondary: str = Field(description="Secondary color")
    accent: str = Field(description="Accent color")
    background: str = Field(description="Background color")
    text: str = Field(description="Text color")
    muted: str = Field(description="Muted color")


class TypographySizes(BaseModel):
    """Typography size definitions."""
    h1: str = Field(description="H1 heading size")
    h2: str = Field(description="H2 heading size")
    h3: str = Field(description="H3 heading size")
    body: str = Field(description="Body text size")


class Typography(BaseModel):
    """Typography system."""
    headingFont: str = Field(description="Font family for headings")
    bodyFont: str = Field(description="Font family for body text")
    sizes: TypographySizes = Field(description="Typography sizes")


class Logo(BaseModel):
    """Logo information."""
    text: str = Field(description="Logo text")
    tagline: str = Field(description="Logo tagline")


class DesignSystem(BaseModel):
    """Complete design system."""
    colorPalette: ColorPalette = Field(description="Color palette")
    typography: Typography = Field(description="Typography system")
    brandPersona: str = Field(description="Brand personality description")
    logo: Logo = Field(description="Logo information")


class SiteSettings(BaseModel):
    """Site-wide settings."""
    title: str = Field(description="Site title")
    description: str = Field(description="Site description")
    keywords: List[str] = Field(description="SEO keywords")
    favicon: str = Field(description="Favicon path")
    ogImage: str = Field(description="Open Graph image path")


class SiteData(BaseModel):
    """Complete site data structure."""
    artisanInfo: ArtisanInfo = Field(description="Artisan business information")
    products: List[Product] = Field(description="List of products", min_length=4)
    galleryItems: List[GalleryItem] = Field(description="List of gallery items", min_length=6)
    navigation: Navigation = Field(description="Navigation structure")
    designSystem: DesignSystem = Field(description="Design system")
    siteSettings: SiteSettings = Field(description="Site settings")
